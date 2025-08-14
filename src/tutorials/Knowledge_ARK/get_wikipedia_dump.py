#!/usr/bin/env python3
"""
Wikipedia dumps fetcher (Python)

Fetch selected Wikipedia dump files for a given project (e.g., enwiki) and
dump date (e.g., latest) within a size budget. Uses dumpstatus.json for an
authoritative file list with sizes and checksums.

Defaults are conservative and useful: pages-articles-multistream (XML), its
index, abstracts, and all-titles-in-ns0.

Destination (default):
  <repo_root>/alden-core/data/archive/wikipedia/<project>/<date>/raw

Examples:
  # Common, under 200 GiB typically
  python alden-core/tools/get_wikipedia_dump.py --project enwiki --date latest \
    --max-gib 300 --concurrency 12

  # Add redirects and categorylinks as well
  python alden-core/tools/get_wikipedia_dump.py --include pages-articles-multistream \
    --include abstracts --include all-titles-in-ns0 --include redirects --include categorylinks
"""

from __future__ import annotations

import argparse
import concurrent.futures
import contextlib
import datetime as dt
import json
import math
import os
import re
import shutil
import sys
import threading
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urljoin


WIKI_DUMPS_ROOT = "https://dumps.wikimedia.org/"


@dataclass(frozen=True)
class RemoteFile:
    filename: str
    url: str
    size_bytes: Optional[int]
    md5: Optional[str]
    sha1: Optional[str]


def create_session(timeout: int = 30) -> requests.Session:
    s = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retries, pool_connections=32, pool_maxsize=32)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    s.headers.update({"User-Agent": "mindgardenai-wiki-fetcher/1.0"})
    orig_request = s.request

    def _request(method, url, **kwargs):
        kwargs.setdefault("timeout", timeout)
        return orig_request(method, url, **kwargs)

    s.request = _request  # type: ignore
    return s


def human_bytes(num: int) -> str:
    if num <= 0:
        return "0 B"
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    power = min(int(math.log(num, 1024)), len(units) - 1)
    return f"{num / (1024 ** power):.2f} {units[power]}"


def free_space_bytes(path: Path) -> int:
    return shutil.disk_usage(path).free


def ensure_parent(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)


def load_dumpstatus(session: requests.Session, project: str, date: str) -> Dict:
    base = urljoin(WIKI_DUMPS_ROOT, f"{project}/{date}/")
    candidates = [
        "dumpstatus.json",
        "dump.json",
        "dumpstatus.json.gz",
    ]

    last_exc: Optional[Exception] = None
    for name in candidates:
        url = urljoin(base, name)
        try:
            r = session.get(url)
            # Some mirrors return 200 with HTML; enforce JSON or gz
            if r.status_code == 404:
                continue
            if name.endswith(".gz"):
                import gzip
                import io as _io

                with gzip.GzipFile(fileobj=_io.BytesIO(r.content)) as gz:
                    data = gz.read().decode("utf-8", errors="replace")
                return json.loads(data)
            else:
                return r.json()
        except Exception as e:
            last_exc = e
            continue

    # Fallback: parse index to locate dumpstatus.json(link)
    try:
        index = session.get(base)
        index.raise_for_status()
        m = re.search(r'href=["\'](dumpstatus\.json(?:\.gz)?)["\']', index.text)
        if m:
            found = m.group(1)
            url = urljoin(base, found)
            r = session.get(url)
            if found.endswith(".gz"):
                import gzip
                import io as _io

                with gzip.GzipFile(fileobj=_io.BytesIO(r.content)) as gz:
                    data = gz.read().decode("utf-8", errors="replace")
                return json.loads(data)
            return r.json()
    except Exception as e:
        last_exc = e

    raise RuntimeError(f"Could not load dumpstatus for {project}/{date} at {base}." )


def parse_directory_for_files(
    session: requests.Session, base_url: str, include_patterns: List[str]
) -> List[RemoteFile]:
    resp = session.get(base_url)
    resp.raise_for_status()
    html = resp.text
    # Gather hrefs ending with common dump extensions
    links = re.findall(r'href=["\']([^"\']+)', html)
    # Build regex list
    regexes = [re.compile(p) for p in include_patterns]

    files: List[RemoteFile] = []
    for href in links:
        if not (href.endswith('.bz2') or href.endswith('.gz') or href.endswith('.zst') or href.endswith('.txt') or href.endswith('.xml')):
            continue
        fname = href.split('/')[-1]
        # Match include patterns
        if not any(r.search(fname) for r in regexes):
            continue
        url = urljoin(base_url, href)
        files.append(RemoteFile(filename=fname, url=url, size_bytes=None, md5=None, sha1=None))
    # De-dup and sort
    unique: Dict[str, RemoteFile] = {f.filename: f for f in files}
    return [unique[k] for k in sorted(unique.keys())]


def select_files_from_dumpstatus(
    dump: Dict, base_url: str, include_patterns: List[str]
) -> List[RemoteFile]:
    # Build regex list
    regexes = [re.compile(p) for p in include_patterns]

    files: List[RemoteFile] = []
    jobs = dump.get("jobs", {})
    for job_name, job in jobs.items():
        job_files = job.get("files") or {}
        # job_files may be dict keyed by filename
        for fname, meta in job_files.items():
            status = meta.get("status")
            # consider only done or available files
            if status not in ("done", "ok", "good", "complete", None):
                continue
            url = meta.get("url")
            # Some dumpstatus entries provide only basename; build full URL if missing
            if not url:
                url = urljoin(base_url, fname)
            size = meta.get("size")
            size_int = int(size) if isinstance(size, (int, float, str)) and str(size).isdigit() else None
            rf = RemoteFile(
                filename=fname,
                url=url,
                size_bytes=size_int,
                md5=meta.get("md5"),
                sha1=meta.get("sha1"),
            )
            # Match include patterns against filename
            if any(r.search(fname) for r in regexes):
                files.append(rf)
    # De-dup by filename
    unique: Dict[str, RemoteFile] = {f.filename: f for f in files}
    return [unique[k] for k in sorted(unique.keys())]


def download_one(session: requests.Session, item: RemoteFile, dest_root: Path) -> Tuple[str, int, bool]:
    dest = dest_root / item.filename
    ensure_parent(dest)

    if dest.exists() and item.size_bytes is not None:
        try:
            if dest.stat().st_size == item.size_bytes:
                return item.filename, 0, True
        except Exception:
            pass

    temp = dest.with_suffix(dest.suffix + ".part")
    written = 0
    print(f"START {item.filename} (expected {human_bytes(item.size_bytes or 0)})", flush=True)
    try:
        with session.get(item.url, stream=True) as r:
            r.raise_for_status()
            with open(temp, "wb") as f:
                last_report = time.time()
                for chunk in r.iter_content(chunk_size=1024 * 1024):
                    if not chunk:
                        continue
                    f.write(chunk)
                    written += len(chunk)
                    now = time.time()
                    if now - last_report >= 2:
                        print(f"PROGRESS {item.filename}: {human_bytes(written)}", flush=True)
                        last_report = now
        if item.size_bytes is not None and written != item.size_bytes:
            raise RuntimeError(
                f"Size mismatch for {item.filename}: expected {item.size_bytes}, got {written}"
            )
        temp.replace(dest)
        print(f"DONE {item.filename}: {human_bytes(written)}", flush=True)
        return item.filename, written, False
    finally:
        with contextlib.suppress(Exception):
            if temp.exists():
                temp.unlink()


def write_manifest(path: Path, meta: Dict, files: List[RemoteFile], downloaded_bytes: int, skipped_count: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "source_root": meta["base_url"],
        "project": meta["project"],
        "date": meta["date"],
        "created_at": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "counts": {
            "total_files_listed": len(files),
            "total_bytes_listed": int(sum(f.size_bytes or 0 for f in files)),
            "downloaded_bytes": int(downloaded_bytes),
            "skipped_existing": int(skipped_count),
        },
        "files": [asdict(f) for f in files],
    }
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Fetch Wikipedia dump files within a size budget")
    ap.add_argument("--project", type=str, default="enwiki", help="Project, e.g., enwiki")
    ap.add_argument("--date", type=str, default="latest", help="Dump date folder, e.g., latest or 20250601")
    ap.add_argument(
        "--include",
        action="append",
        default=[
            r"pages-articles-multistream(\.xml(\.bz2|\.zst))?$",
            r"pages-articles-multistream-index(\.txt(\.bz2|\.zst))?$",
            r"abstracts(\.xml(\.gz|\.bz2|\.zst))?$",
            r"all-titles-in-ns0(\.gz|\.bz2|\.zst)?$",
        ],
        help="Regex patterns of filenames to include (repeatable)",
    )
    ap.add_argument("--dest-root", type=Path, default=None, help="Destination root directory")
    ap.add_argument("--max-gib", type=float, default=300.0, help="Max new bytes to download")
    ap.add_argument("--reserve-free-gib", type=float, default=20.0, help="Free space to leave")
    ap.add_argument("--concurrency", type=int, default=8, help="Concurrent downloads")
    ap.add_argument("--dry-run", action="store_true", help="List only; no downloads")
    ap.add_argument("--no-manifest", action="store_true", help="Skip writing manifest")

    args = ap.parse_args(argv)

    # Destination default
    if args.dest_root is None:
        repo_root = Path(__file__).resolve().parents[2]
        date_str = args.date
        args.dest_root = (
            repo_root
            / "alden-core"
            / "data"
            / "archive"
            / "wikipedia"
            / args.project
            / date_str
            / "raw"
        )
    dest: Path = args.dest_root
    dest.mkdir(parents=True, exist_ok=True)

    session = create_session()
    base_url = urljoin(WIKI_DUMPS_ROOT, f"{args.project}/{args.date}/")

    print(f"Loading dumpstatus: {base_url}dumpstatus.json")
    try:
        dump = load_dumpstatus(session, args.project, args.date)
        files = select_files_from_dumpstatus(dump, base_url, args.include)
    except Exception as e:
        print(f"Warn: dumpstatus not available ({e}); falling back to directory parse.")
        files = parse_directory_for_files(session, base_url, args.include)
    if not files:
        print("No files selected by the include patterns.")
        return 1

    total_bytes = int(sum(f.size_bytes or 0 for f in files))
    print(f"Selected {len(files)} files totaling {human_bytes(total_bytes)}")

    # Skip existing
    remaining: List[RemoteFile] = []
    skipped_count = 0
    existing_bytes = 0
    for rf in files:
        p = dest / rf.filename
        if p.exists() and rf.size_bytes is not None and p.stat().st_size == rf.size_bytes:
            skipped_count += 1
            existing_bytes += rf.size_bytes
        else:
            remaining.append(rf)

    print(f"Existing matched: {skipped_count} ({human_bytes(existing_bytes)}); remaining: {len(remaining)}")

    budget_bytes = int(args.max_gib * (1024 ** 3))
    reserve_bytes = int(args.reserve_free_gib * (1024 ** 3))

    if args.dry_run:
        if not args.no_manifest:
            manifest_path = dest.parent / "manifests" / "wikipedia_manifest.json"
            write_manifest(
                manifest_path,
                {"project": args.project, "date": args.date, "base_url": base_url},
                files,
                0,
                skipped_count,
            )
            print(f"Manifest written: {manifest_path}")
        return 0

    downloaded_bytes = 0
    downloaded_count = 0
    lock = threading.Lock()

    def can_schedule(next_size: Optional[int]) -> bool:
        if free_space_bytes(dest) <= reserve_bytes:
            return False
        if next_size is None:
            return True
        with lock:
            return (downloaded_bytes + next_size) <= budget_bytes

    remaining_sorted = sorted(remaining, key=lambda f: f.filename)
    print(
        f"Starting downloads with concurrency={args.concurrency}, budget={human_bytes(budget_bytes)}, reserve={human_bytes(reserve_bytes)}"
    )

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures: List[concurrent.futures.Future] = []
        for rf in remaining_sorted:
            if not can_schedule(rf.size_bytes):
                break
            futures.append(pool.submit(download_one, session, rf, dest))

        for fut in concurrent.futures.as_completed(futures):
            try:
                fname, bytes_dl, skipped = fut.result()
            except Exception as e:
                print(f"ERROR: {e}")
                continue
            with lock:
                downloaded_bytes += bytes_dl
                if not skipped:
                    downloaded_count += 1
            print(f"{fname} -> {'skipped' if skipped else human_bytes(bytes_dl)}")

    print(f"Downloaded {downloaded_count} files totaling {human_bytes(downloaded_bytes)}")
    if not args.no_manifest:
        manifest_path = dest.parent / "manifests" / "wikipedia_manifest.json"
        write_manifest(
            manifest_path,
            {"project": args.project, "date": args.date, "base_url": base_url},
            files,
            downloaded_bytes,
            skipped_count,
        )
        print(f"Manifest written: {manifest_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())


