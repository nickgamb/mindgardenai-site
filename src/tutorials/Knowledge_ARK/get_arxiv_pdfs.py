#!/usr/bin/env python3
"""
arXiv PDFs fetcher (Python)

Fetch as many arXiv PDFs as fit a size budget from the public requester-pays
S3 bucket, preserving structure, with optional date/prefix filters and resume.

Bucket: s3://arxiv/pdf/
REST:   https://arxiv.s3.amazonaws.com/?list-type=2&prefix=pdf/

Important: This is a requester-pays bucket. We include header
  x-amz-request-payer: requester
for both listing and GET. You are responsible for data transfer costs.

Default destination:
  <repo_root>/alden-core/data/archive/arxiv/<YYYYMMDD>/raw/pdf

Examples:
  # Download up to 480 GiB, keep 20 GiB free, 12 workers
  python alden-core/tools/get_arxiv_pdfs.py --max-gib 480 --concurrency 12

  # Only recent uploads/updates (by LastModified in S3) since 2025-01-01
  python alden-core/tools/get_arxiv_pdfs.py --start-date 2025-01-01 --max-gib 200

  # Limit to a key prefix (e.g., monthly folder if present)
  python alden-core/tools/get_arxiv_pdfs.py --prefix pdf/2506/ --max-gib 100
"""

from __future__ import annotations

import argparse
import concurrent.futures
import contextlib
import datetime as dt
import json
import math
import os
import shutil
import sys
import threading
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import List, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urljoin


S3_ENDPOINT = "https://arxiv.s3.amazonaws.com"
DEFAULT_PREFIX = "pdf/"


@dataclass(frozen=True)
class RemoteFile:
    key: str
    size_bytes: Optional[int]
    last_modified: Optional[str]

    @property
    def url(self) -> str:
        return urljoin(S3_ENDPOINT + "/", self.key)

    @property
    def relative_path(self) -> str:
        # Drop leading 'pdf/' for local layout
        if self.key.startswith(DEFAULT_PREFIX):
            return self.key[len(DEFAULT_PREFIX) :]
        return self.key


def create_session(timeout: int = 30) -> requests.Session:
    s = requests.Session()
    retries = Retry(
        total=5, backoff_factor=0.5, status_forcelist=[429, 500, 502, 503, 504], allowed_methods=["GET"]
    )
    adapter = HTTPAdapter(max_retries=retries, pool_connections=32, pool_maxsize=32)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    s.headers.update({
        "User-Agent": "mindgardenai-arxiv-fetcher/1.0",
        "x-amz-request-payer": "requester",
    })
    # default timeouts via wrapper
    orig_request = s.request

    def _request(method, url, **kwargs):
        kwargs.setdefault("timeout", timeout)
        return orig_request(method, url, **kwargs)

    s.request = _request  # type: ignore
    return s


def list_s3_objects(
    session: requests.Session,
    prefix: str,
    start_after: Optional[str] = None,
) -> Tuple[List[RemoteFile], Optional[str]]:
    params = {
        "list-type": "2",
        "prefix": prefix,
        "max-keys": "1000",
    }
    if start_after:
        params["start-after"] = start_after

    r = session.get(S3_ENDPOINT, params=params)
    r.raise_for_status()
    text = r.text

    root = ET.fromstring(text)

    def findall(elem, name):
        # Handle possible missing xmlns by trying both
        res = elem.findall(name)
        if res:
            return res
        return elem.findall(f"{{http://s3.amazonaws.com/doc/2006-03-01/}}{name}")

    files: List[RemoteFile] = []
    for c in findall(root, "Contents"):
        key_el = c.find("Key") or c.find("{http://s3.amazonaws.com/doc/2006-03-01/}Key")
        size_el = c.find("Size") or c.find("{http://s3.amazonaws.com/doc/2006-03-01/}Size")
        lm_el = c.find("LastModified") or c.find("{http://s3.amazonaws.com/doc/2006-03-01/}LastModified")
        if key_el is None:
            continue
        key = key_el.text or ""
        if not key.endswith(".pdf"):
            continue
        try:
            size = int(size_el.text) if size_el is not None else None
        except Exception:
            size = None
        last_modified = lm_el.text if lm_el is not None else None
        files.append(RemoteFile(key=key, size_bytes=size, last_modified=last_modified))

    is_trunc_el = root.find("IsTruncated") or root.find("{http://s3.amazonaws.com/doc/2006-03-01/}IsTruncated")
    is_truncated = (is_trunc_el is not None and (is_trunc_el.text or "").lower() == "true")
    next_start_after: Optional[str] = None
    if is_truncated:
        # Use the last key as the next start-after
        if files:
            next_start_after = files[-1].key

    return files, next_start_after


def parse_date(s: Optional[str]) -> Optional[dt.datetime]:
    if not s:
        return None
    # Support YYYY-MM-DD
    return dt.datetime.strptime(s, "%Y-%m-%d")


def within_date(last_modified: Optional[str], start: Optional[dt.datetime], end: Optional[dt.datetime]) -> bool:
    if start is None and end is None:
        return True
    if not last_modified:
        return False
    # Example format: 2025-06-01T00:12:34.000Z
    try:
        lm = dt.datetime.fromisoformat(last_modified.replace("Z", "+00:00"))
    except Exception:
        return False
    if start and lm < start:
        return False
    if end and lm > end:
        return False
    return True


def human_bytes(num: int) -> str:
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    if num <= 0:
        return "0 B"
    power = min(int(math.log(num, 1024)), len(units) - 1)
    return f"{num / (1024 ** power):.2f} {units[power]}"


def free_space_bytes(path: Path) -> int:
    return shutil.disk_usage(path).free


def ensure_parent(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)


def download_one(session: requests.Session, item: RemoteFile, dest_root: Path) -> Tuple[str, int, bool]:
    rel = item.relative_path
    dest = dest_root / rel
    ensure_parent(dest)

    if dest.exists() and item.size_bytes is not None:
        try:
            if dest.stat().st_size == item.size_bytes:
                return rel, 0, True
        except Exception:
            pass

    temp = dest.with_suffix(dest.suffix + ".part")
    written = 0
    print(f"START {rel} (expected {human_bytes(item.size_bytes or 0)})", flush=True)
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
                        print(f"PROGRESS {rel}: {human_bytes(written)}", flush=True)
                        last_report = now
        if item.size_bytes is not None and written != item.size_bytes:
            raise RuntimeError(
                f"Size mismatch for {rel}: expected {item.size_bytes}, got {written}"
            )
        temp.replace(dest)
        print(f"DONE {rel}: {human_bytes(written)}", flush=True)
        return rel, written, False
    finally:
        with contextlib.suppress(Exception):
            if temp.exists():
                temp.unlink()


def write_manifest(path: Path, files: List[RemoteFile], downloaded_bytes: int, skipped_count: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "source_root": f"{S3_ENDPOINT}/?list-type=2&prefix={DEFAULT_PREFIX}",
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
    ap = argparse.ArgumentParser(description="Fetch arXiv PDFs from S3 within a size budget")
    ap.add_argument("--dest-root", type=Path, default=None, help="Destination root; default is archive/arxiv/<YYYYMMDD>/raw/pdf")
    ap.add_argument("--prefix", type=str, default=DEFAULT_PREFIX, help="S3 key prefix (default: pdf/)")
    ap.add_argument("--start-date", type=str, default=None, help="Filter by LastModified >= YYYY-MM-DD")
    ap.add_argument("--end-date", type=str, default=None, help="Filter by LastModified <= YYYY-MM-DD")
    ap.add_argument("--max-gib", type=float, default=480.0, help="Maximum new bytes to download")
    ap.add_argument("--reserve-free-gib", type=float, default=20.0, help="Minimum free space to leave")
    ap.add_argument("--concurrency", type=int, default=8, help="Concurrent downloads")
    ap.add_argument("--dry-run", action="store_true", help="Do not download; only list and manifest")
    ap.add_argument("--no-manifest", action="store_true", help="Skip writing manifest")

    args = ap.parse_args(argv)

    # Destination default
    if args.dest_root is None:
        repo_root = Path(__file__).resolve().parents[2]
        date_str = dt.datetime.utcnow().strftime("%Y%m%d")
        args.dest_root = repo_root / "alden-core" / "data" / "archive" / "arxiv" / date_str / "raw" / "pdf"
    dest: Path = args.dest_root
    dest.mkdir(parents=True, exist_ok=True)

    session = create_session()

    start_dt = parse_date(args.start_date)
    end_dt = parse_date(args.end_date)

    # Enumerate
    print(f"Enumerating S3 objects under prefix: {args.prefix}")
    listed: List[RemoteFile] = []
    start_after: Optional[str] = None
    while True:
        batch, start_after = list_s3_objects(session, args.prefix, start_after)
        if not batch:
            break
        if start_dt or end_dt:
            batch = [b for b in batch if within_date(b.last_modified, start_dt, end_dt)]
        listed.extend(batch)
        print(f"  ... total discovered: {len(listed)}")
        if start_after is None:
            break

    if not listed:
        print("No files discovered for the given filters.")
        return 1

    total_bytes = int(sum(f.size_bytes or 0 for f in listed))
    print(f"Discovered {len(listed)} files; total size listed: {human_bytes(total_bytes)}")

    # Skip existing
    remaining: List[RemoteFile] = []
    skipped_count = 0
    existing_bytes = 0
    for rf in listed:
        p = dest / rf.relative_path
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
            manifest_path = dest.parent.parent / "manifests" / "arxiv_pdfs_manifest.json"
            write_manifest(manifest_path, listed, 0, skipped_count)
            print(f"Manifest written: {manifest_path}")
        return 0

    # Plan & download
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

    remaining_sorted = sorted(remaining, key=lambda f: f.relative_path)
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
                rel, bytes_dl, skipped = fut.result()
            except Exception as e:
                print(f"ERROR: {e}")
                continue
            with lock:
                downloaded_bytes += bytes_dl
                if not skipped:
                    downloaded_count += 1
            print(f"{rel} -> {'skipped' if skipped else human_bytes(bytes_dl)}")

    print(f"Downloaded {downloaded_count} files totaling {human_bytes(downloaded_bytes)}")
    if not args.no_manifest:
        manifest_path = dest.parent.parent / "manifests" / "arxiv_pdfs_manifest.json"
        write_manifest(manifest_path, listed, downloaded_bytes, skipped_count)
        print(f"Manifest written: {manifest_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())


