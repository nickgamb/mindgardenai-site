#!/usr/bin/env python3
"""
Project Gutenberg fetcher (Python)

Fetches Project Gutenberg metadata (RDF catalog) and then downloads selected
books (preferred formats) within a size budget, with concurrency, resume, and
manifest output. Respects your chosen languages and license filters.

Catalog source (metadata):
  https://www.gutenberg.org/cache/epub/feeds/rdf-files.tar.bz2

Default destination:
  <repo_root>/alden-core/data/archive/gutenberg/<YYYYMMDD>/raw

Examples:
  # Metadata + English public-domain EPUB (images) and UTF-8 text
  python alden-core/tools/get_gutenberg.py --max-gib 200 --concurrency 8

  # Reuse existing local catalog tarball
  python alden-core/tools/get_gutenberg.py --catalog-path D:\\tmp\\rdf-files.tar.bz2 --max-gib 200

Notes:
  - Please be considerate to Gutenberg; default concurrency is small.
  - Prefer downloading from the cache URLs contained in the RDF (stable).
"""

from __future__ import annotations

import argparse
import bz2
import concurrent.futures
import contextlib
import datetime as dt
import io
import json
import math
import os
import re
import shutil
import sys
import tarfile
import threading
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


CATALOG_URL = "https://www.gutenberg.org/cache/epub/feeds/rdf-files.tar.bz2"


@dataclass(frozen=True)
class GutenbergFile:
    id: int
    url: str
    media_type: str  # e.g., application/epub+zip or text/plain; charset=utf-8
    size_bytes: Optional[int]
    language: Optional[str]
    rights: Optional[str]

    @property
    def filename(self) -> str:
        # Derive a readable filename from URL
        name = self.url.rstrip("/").split("/")[-1]
        if not name:
            name = f"pg{self.id}"
        return f"{self.id}/{name}"


def create_session(timeout: int = 30) -> requests.Session:
    s = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retries, pool_connections=16, pool_maxsize=16)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    s.headers.update({"User-Agent": "mindgardenai-gutenberg-fetcher/1.0"})
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


def download_file(session: requests.Session, url: str, dest: Path) -> int:
    ensure_parent(dest)
    temp = dest.with_suffix(dest.suffix + ".part")
    written = 0
    with session.get(url, stream=True) as r:
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
                    print(f"PROGRESS {dest.name}: {human_bytes(written)}", flush=True)
                    last_report = now
    temp.replace(dest)
    return written


def fetch_catalog(session: requests.Session, dest_dir: Path, catalog_url: str, catalog_path: Optional[Path]) -> Path:
    dest_dir.mkdir(parents=True, exist_ok=True)
    if catalog_path and catalog_path.exists():
        return catalog_path
    out = dest_dir / "rdf-files.tar.bz2"
    if out.exists() and out.stat().st_size > 0:
        return out
    print(f"Downloading catalog: {catalog_url}")
    download_file(session, catalog_url, out)
    return out


def parse_rdf_catalog(
    tar_bz2_path: Path,
    languages: List[str],
    media_type_whitelist: List[str],
    rights_allow: List[str],
    limit_items: Optional[int] = None,
) -> List[GutenbergFile]:
    lang_set = {l.lower() for l in languages}
    mt_set = {m.lower() for m in media_type_whitelist}
    rights_allow_set = {r.lower() for r in rights_allow}

    results: List[GutenbergFile] = []
    count_items = 0

    print(f"Parsing catalog: {tar_bz2_path}")
    with bz2.open(tar_bz2_path, "rb") as bzfp:
        with tarfile.open(fileobj=bzfp, mode="r:") as tar:
            for member in tar:  # type: ignore
                if not member.isfile() or not member.name.endswith(".rdf"):
                    continue
                f = tar.extractfile(member)
                if f is None:
                    continue
                try:
                    tree = ET.parse(f)
                    root = tree.getroot()
                except Exception:
                    continue

                # Namespaces used in Gutenberg RDF
                ns = {
                    "pg": "http://www.gutenberg.org/2009/pgterms/",
                    "dcterms": "http://purl.org/dc/terms/",
                    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                }

                # Book id
                ebook_el = root.find(".//pg:ebook", ns)
                if ebook_el is None:
                    continue
                about = ebook_el.attrib.get(f"{{{ns['rdf']}}}about", "")
                m = re.search(r"(\d+)$", about)
                if not m:
                    continue
                book_id = int(m.group(1))

                # Language(s)
                langs: List[str] = []
                for lang_el in root.findall(".//dcterms:language//rdf:value", ns):
                    if lang_el.text:
                        langs.append(lang_el.text.lower())

                lang_ok = (not lang_set) or any(l in lang_set for l in langs) or ("en" in lang_set and not langs)

                # Rights
                rights_text = None
                r_el = root.find(".//dcterms:rights", ns)
                if r_el is not None and r_el.text:
                    rights_text = r_el.text.strip()
                rights_ok = (not rights_allow_set) or (rights_text and any(x in rights_text.lower() for x in rights_allow_set))

                if not (lang_ok and rights_ok):
                    continue

                # Available files
                for file_el in root.findall(".//pg:file", ns):
                    url = file_el.attrib.get(f"{{{ns['rdf']}}}about")
                    if not url:
                        continue
                    fmt_el = file_el.find(".//dcterms:format//rdf:Description//rdf:value", ns)
                    media_type = (fmt_el.text if fmt_el is not None and fmt_el.text else "").lower()
                    if mt_set and media_type not in mt_set:
                        continue
                    size_el = file_el.find(".//pg:file-size", ns)
                    size_bytes = None
                    if size_el is not None and size_el.text and size_el.text.isdigit():
                        size_bytes = int(size_el.text)
                    results.append(
                        GutenbergFile(
                            id=book_id,
                            url=url,
                            media_type=media_type,
                            size_bytes=size_bytes,
                            language=langs[0] if langs else None,
                            rights=rights_text,
                        )
                    )

                count_items += 1
                if limit_items and count_items >= limit_items:
                    break

    # Deduplicate by (id, url)
    seen = set()
    unique: List[GutenbergFile] = []
    for gf in results:
        key = (gf.id, gf.url)
        if key in seen:
            continue
        seen.add(key)
        unique.append(gf)
    return unique


def download_one(session: requests.Session, item: GutenbergFile, dest_root: Path) -> Tuple[str, int, bool]:
    dest = dest_root / item.filename
    ensure_parent(dest)
    if dest.exists() and item.size_bytes is not None:
        try:
            if dest.stat().st_size == item.size_bytes:
                return item.filename, 0, True
        except Exception:
            pass
    print(f"START {item.filename} ({item.media_type}; expected {human_bytes(item.size_bytes or 0)})", flush=True)
    try:
        written = download_file(session, item.url, dest)
        print(f"DONE {item.filename}: {human_bytes(written)}", flush=True)
        return item.filename, written, False
    except Exception as e:
        # Clean up partial
        with contextlib.suppress(Exception):
            if dest.exists() and dest.stat().st_size == 0:
                dest.unlink()
        raise e


def write_manifest(path: Path, files: List[GutenbergFile], downloaded_bytes: int, skipped_count: int, meta: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "source_catalog": CATALOG_URL,
        "created_at": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "counts": {
            "total_files_listed": len(files),
            "total_bytes_listed": int(sum(f.size_bytes or 0 for f in files)),
            "downloaded_bytes": int(downloaded_bytes),
            "skipped_existing": int(skipped_count),
        },
        "filters": meta,
        "files": [asdict(f) for f in files],
    }
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Fetch Project Gutenberg content within a size budget")
    ap.add_argument("--dest-root", type=Path, default=None, help="Destination root (default archive/gutenberg/<YYYYMMDD>/raw)")
    ap.add_argument("--max-gib", type=float, default=200.0, help="Maximum new bytes to download")
    ap.add_argument("--reserve-free-gib", type=float, default=20.0, help="Minimum free space to leave")
    ap.add_argument("--concurrency", type=int, default=6, help="Concurrent downloads (be considerate)")
    ap.add_argument("--languages", nargs="*", default=["en"], help="Languages to include (ISO strings)")
    ap.add_argument(
        "--media-types",
        nargs="*",
        default=["application/epub+zip", "text/plain; charset=utf-8"],
        help="Media types to include",
    )
    ap.add_argument(
        "--rights-allow",
        nargs="*",
        default=["public domain"],
        help="Substring filters for rights (e.g., 'public domain')",
    )
    ap.add_argument("--catalog-url", type=str, default=CATALOG_URL, help="Catalog URL (RDF tar.bz2)")
    ap.add_argument("--catalog-path", type=Path, default=None, help="Use local catalog tar.bz2 if provided")
    ap.add_argument("--limit-items", type=int, default=None, help="Parse only first N RDF records (speed up testing)")
    ap.add_argument("--dry-run", action="store_true", help="List only; no downloads")
    ap.add_argument("--no-manifest", action="store_true", help="Skip manifest writing")

    args = ap.parse_args(argv)

    # Destination default
    if args.dest_root is None:
        repo_root = Path(__file__).resolve().parents[2]
        date_str = dt.datetime.utcnow().strftime("%Y%m%d")
        args.dest_root = repo_root / "alden-core" / "data" / "archive" / "gutenberg" / date_str / "raw"
    dest: Path = args.dest_root
    dest.mkdir(parents=True, exist_ok=True)

    session = create_session()

    # Fetch catalog
    meta_dir = dest.parent / "metadata"
    catalog_path = fetch_catalog(session, meta_dir, args.catalog_url, args.catalog_path)

    # Parse RDF and select files
    files = parse_rdf_catalog(
        catalog_path,
        languages=args.languages,
        media_type_whitelist=args.media_types,
        rights_allow=args.rights_allow,
        limit_items=args.limit_items,
    )
    if not files:
        print("No files matched the filters.")
        return 1

    total_bytes = int(sum(f.size_bytes or 0 for f in files))
    print(f"Matched {len(files)} files totaling {human_bytes(total_bytes)}")

    # Skip existing
    remaining: List[GutenbergFile] = []
    skipped_count = 0
    existing_bytes = 0
    for gf in files:
        p = dest / gf.filename
        if p.exists() and gf.size_bytes is not None and p.stat().st_size == gf.size_bytes:
            skipped_count += 1
            existing_bytes += gf.size_bytes
        else:
            remaining.append(gf)
    print(f"Existing matched: {skipped_count} ({human_bytes(existing_bytes)}); remaining: {len(remaining)}")

    if args.dry_run:
        if not args.no_manifest:
            manifest_path = dest.parent / "manifests" / "gutenberg_manifest.json"
            write_manifest(
                manifest_path,
                files,
                0,
                skipped_count,
                meta={
                    "languages": args.languages,
                    "media_types": args.media_types,
                    "rights_allow": args.rights_allow,
                },
            )
            print(f"Manifest written: {manifest_path}")
        return 0

    budget_bytes = int(args.max_gib * (1024 ** 3))
    reserve_bytes = int(args.reserve_free_gib * (1024 ** 3))

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
        for gf in remaining_sorted:
            if not can_schedule(gf.size_bytes):
                break
            futures.append(pool.submit(download_one, session, gf, dest))

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
        manifest_path = dest.parent / "manifests" / "gutenberg_manifest.json"
        write_manifest(
            manifest_path,
            files,
            downloaded_bytes,
            skipped_count,
            meta={
                "languages": args.languages,
                "media_types": args.media_types,
                "rights_allow": args.rights_allow,
            },
        )
        print(f"Manifest written: {manifest_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())



