#!/usr/bin/env python3
"""
OpenAlex Works fetcher (Python)

Purpose:
- Recursively discover and download as many OpenAlex "works" files as will fit
  under a specified size budget and free-space reserve.
- Preserves directory structure under an immutable, date-stamped snapshot path.
- Skips files that already exist with matching size. Resumes safely across runs.
- Writes a MANIFEST.json with counts and byte totals for verification.

Default destination:
  <repo_root>/alden-core/data/archive/openalex/<YYYYMMDD>/raw/works

Example:
  python alden-core/tools/get_openalex_works.py --max-gib 480 --concurrency 8

Notes:
- This script focuses on the "works" entity under
  https://files.openalex.org/data/works/
- It uses simple HTML link discovery for directory listings.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import contextlib
import functools
import dataclasses
import datetime as dt
import hashlib
import json
import math
import os
import queue
import re
import xml.etree.ElementTree as ET
import shutil
import sys
import threading
import time
from pathlib import Path
from typing import Iterable, List, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from urllib.parse import urljoin, urlparse


OPENALEX_WORKS_ROOT = "https://files.openalex.org/data/works/"
S3_LIST_ENDPOINT = "https://openalex.s3.amazonaws.com"


@dataclasses.dataclass(frozen=True)
class RemoteFile:
    url: str
    relative_path: str
    size_bytes: Optional[int]


def create_requests_session(total_timeout: int = 30) -> requests.Session:
    session = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retries, pool_connections=32, pool_maxsize=32)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    session.headers.update({"User-Agent": "mindgardenai-openalex-fetcher/1.0"})
    session.request = functools.partial(session.request, timeout=total_timeout)  # type: ignore
    return session


def list_directory_links(session: requests.Session, base_url: str) -> List[str]:
    resp = session.get(base_url)
    resp.raise_for_status()
    html = resp.text
    # Simple href extraction for .gz files and subdirectories
    hrefs = re.findall(r'href=[\"\']([^\"\']+)', html)
    links: List[str] = []
    for href in hrefs:
        if href in ("../", "./"):
            continue
        # Normalize to absolute URL
        abs_url = urljoin(base_url, href)
        links.append(abs_url)
    return links


def discover_all_gz(session: requests.Session, root_url: str) -> List[str]:
    to_visit: queue.SimpleQueue[str] = queue.SimpleQueue()
    seen: set[str] = set()
    gz_files: List[str] = []

    to_visit.put(root_url)
    seen.add(root_url)

    while not to_visit.empty():
        current = to_visit.get()
        try:
            links = list_directory_links(session, current)
        except Exception:
            continue

        for link in links:
            if link.endswith(".gz"):
                gz_files.append(link)
            else:
                # Heuristic: treat as directory if it ends with '/'
                if link.endswith("/") and link not in seen:
                    seen.add(link)
                    to_visit.put(link)
    return sorted(set(gz_files))


def s3_list_all_gz_under_works(session: requests.Session) -> List[RemoteFile]:
    """
    Uses S3 ListObjectsV2 (anonymous) to enumerate all .gz keys under data/works/.
    Returns RemoteFile entries with url mapped to files.openalex.org and sizes from S3.
    """
    remote_files: List[RemoteFile] = []
    prefix = "data/works/"

    continuation: Optional[str] = None
    while True:
        params = {
            "list-type": "2",
            "prefix": prefix,
            "max-keys": "1000",
        }
        if continuation:
            params["continuation-token"] = continuation

        resp = session.get(S3_LIST_ENDPOINT, params=params)
        resp.raise_for_status()

        # Parse XML
        root = ET.fromstring(resp.text)
        ns = {"s3": "http://s3.amazonaws.com/doc/2006-03-01/"}
        # In practice, many public buckets omit explicit xmlns; handle both cases
        # Try without namespaces first
        def findall(elem, path):
            found = elem.findall(path)
            if found:
                return found
            return elem.findall(path.replace("Contents", "{http://s3.amazonaws.com/doc/2006-03-01/}Contents").replace("Key", "{http://s3.amazonaws.com/doc/2006-03-01/}Key").replace("Size", "{http://s3.amazonaws.com/doc/2006-03-01/}Size").replace("IsTruncated", "{http://s3.amazonaws.com/doc/2006-03-01/}IsTruncated").replace("NextContinuationToken", "{http://s3.amazonaws.com/doc/2006-03-01/}NextContinuationToken"))

        contents = findall(root, "Contents")
        for c in contents:
            key_el = c.find("Key") or c.find("{http://s3.amazonaws.com/doc/2006-03-01/}Key")
            size_el = c.find("Size") or c.find("{http://s3.amazonaws.com/doc/2006-03-01/}Size")
            if key_el is None or size_el is None:
                continue
            key = key_el.text or ""
            if not key.endswith(".gz"):
                continue
            try:
                size = int(size_el.text or "0")
            except Exception:
                size = None
            # Build files.openalex.org URL
            url = urljoin("https://files.openalex.org/", key)
            rel = key[len(prefix) :]
            remote_files.append(RemoteFile(url=url, relative_path=rel, size_bytes=size))

        # Pagination
        is_trunc = root.find("IsTruncated") or root.find("{http://s3.amazonaws.com/doc/2006-03-01/}IsTruncated")
        next_token = root.find("NextContinuationToken") or root.find("{http://s3.amazonaws.com/doc/2006-03-01/}NextContinuationToken")
        more = (is_trunc is not None and (is_trunc.text or "").lower() == "true")
        if more and next_token is not None and next_token.text:
            continuation = next_token.text
        else:
            break

    # De-dup in case of any duplicates
    dedup: dict[str, RemoteFile] = {f.relative_path: f for f in remote_files}
    return [dedup[k] for k in sorted(dedup.keys())]


def head_content_length(session: requests.Session, url: str) -> Optional[int]:
    try:
        resp = session.head(url, allow_redirects=True)
        if resp.status_code >= 400:
            return None
        cl = resp.headers.get("Content-Length")
        if cl is None:
            return None
        return int(cl)
    except Exception:
        return None


def map_url_to_relative_path(url: str, root_url: str) -> str:
    # Preserve the path under works/ exactly
    parsed = urlparse(url)
    parsed_root = urlparse(root_url)
    if parsed.netloc != parsed_root.netloc:
        # Fallback: use entire path
        return parsed.path.lstrip("/")
    if not parsed.path.startswith(parsed_root.path):
        return parsed.path.lstrip("/")
    rel = parsed.path[len(parsed_root.path) :].lstrip("/")
    return rel.replace("\\", "/")


def get_free_space_bytes(path: Path) -> int:
    usage = shutil.disk_usage(path)
    return usage.free


def human_bytes(num: int) -> str:
    units = ["B", "KiB", "MiB", "GiB", "TiB"]
    if num <= 0:
        return "0 B"
    power = min(int(math.log(num, 1024)), len(units) - 1)
    return f"{num / (1024 ** power):.2f} {units[power]}"


def ensure_parent_dir(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def download_one(
    session: requests.Session,
    item: RemoteFile,
    dest_root: Path,
    *,
    prefer_s3_download: bool = False,
) -> Tuple[str, int, bool]:
    # Returns: (relative_path, bytes_downloaded, skipped)
    rel_path = item.relative_path
    dest_path = dest_root / rel_path
    ensure_parent_dir(dest_path)

    # Skip if exists with same size
    if dest_path.exists() and item.size_bytes is not None:
        try:
            if dest_path.stat().st_size == item.size_bytes:
                return (rel_path, 0, True)
        except Exception:
            pass

    # Stream download to a temp file then move
    temp_path = dest_path.with_suffix(dest_path.suffix + ".part")
    bytes_written = 0
    # Build attempt order: CDN then S3, or S3 then CDN
    cdn_url = item.url
    s3_url = urljoin(S3_LIST_ENDPOINT + "/", "data/works/" + rel_path)
    attempt_order = [s3_url, cdn_url] if prefer_s3_download else [cdn_url, s3_url]

    last_exc: Optional[Exception] = None
    for idx, download_url in enumerate(attempt_order):
        try:
            print(
                f"START {rel_path} via {'S3' if download_url == s3_url else 'CDN'} (expected {human_bytes(item.size_bytes or 0)})",
                flush=True,
            )
            with session.get(download_url, stream=True, timeout=(15, 90)) as r:
                r.raise_for_status()
                with open(temp_path, "wb") as f:
                    last_report = time.time()
                    for chunk in r.iter_content(chunk_size=1024 * 1024):
                        if not chunk:
                            continue
                        f.write(chunk)
                        bytes_written += len(chunk)
                        now = time.time()
                        if now - last_report >= 2:
                            print(
                                f"PROGRESS {rel_path}: {human_bytes(bytes_written)}",
                                flush=True,
                            )
                            last_report = now
            # If expected size known, verify size
            if item.size_bytes is not None and bytes_written != item.size_bytes:
                raise RuntimeError(
                    f"Size mismatch for {rel_path}: expected {item.size_bytes}, got {bytes_written}"
                )
            temp_path.replace(dest_path)
            print(
                f"DONE {rel_path}: {human_bytes(bytes_written)}",
                flush=True,
            )
            return (rel_path, bytes_written, False)
        except Exception as e:
            last_exc = e
            print(f"RETRY {rel_path} via alternate path due to: {e}", flush=True)
            # Clean up partial file before next attempt
            with contextlib.suppress(Exception):
                if temp_path.exists():
                    temp_path.unlink()
            bytes_written = 0
            continue
    # If both attempts failed, raise the last exception
    raise last_exc if last_exc else RuntimeError(f"Failed to download {rel_path}")


def write_manifest(
    manifest_path: Path,
    files: List[RemoteFile],
    downloaded_total: int,
    skipped_count: int,
) -> None:
    manifest = {
        "source_root": OPENALEX_WORKS_ROOT,
        "created_at": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "files": [dataclasses.asdict(f) for f in files],
        "counts": {
            "total_files_listed": len(files),
            "total_bytes_listed": sum(f.size_bytes or 0 for f in files),
            "downloaded_bytes": downloaded_total,
            "skipped_existing": skipped_count,
        },
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Fetch OpenAlex works data within a size budget")
    parser.add_argument(
        "--dest-root",
        type=Path,
        default=None,
        help="Destination root directory. Default: <repo_root>/alden-core/data/archive/openalex/<YYYYMMDD>/raw/works",
    )
    parser.add_argument("--max-gib", type=float, default=480.0, help="Maximum new bytes to download (GiB)")
    parser.add_argument(
        "--reserve-free-gib",
        type=float,
        default=20.0,
        help="Leave at least this many GiB free on the destination filesystem",
    )
    parser.add_argument("--concurrency", type=int, default=8, help="Concurrent download workers")
    parser.add_argument(
        "--prefer-s3",
        action="store_true",
        help="Download from S3 endpoint instead of files CDN (can be faster or slower depending on your network)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List what would be downloaded and exit",
    )
    parser.add_argument(
        "--no-manifest",
        action="store_true",
        help="Do not write MANIFEST.json",
    )

    args = parser.parse_args(argv)

    # Compute default destination if not provided
    if args.dest_root is None:
        repo_root = Path(__file__).resolve().parents[2]
        date_str = dt.datetime.utcnow().strftime("%Y%m%d")
        args.dest_root = repo_root / "alden-core" / "data" / "archive" / "openalex" / date_str / "raw" / "works"

    dest_root: Path = args.dest_root
    dest_root.mkdir(parents=True, exist_ok=True)

    session = create_requests_session()

    print(f"Discovering .gz files under: {OPENALEX_WORKS_ROOT}")
    # Prefer S3 ListObjects (reliable) over HTML crawling
    remote_files = s3_list_all_gz_under_works(session)
    if not remote_files:
        # Fallback to HTML crawl if S3 listing fails
        gz_urls = discover_all_gz(session, OPENALEX_WORKS_ROOT)
        if not gz_urls:
            print("No files discovered via S3 or HTML. Exiting.")
            return 1
        print(f"Discovered {len(gz_urls)} files via HTML; querying sizes...")
        remote_files = []
        for url in gz_urls:
            size_bytes = head_content_length(session, url)
            rel_path = map_url_to_relative_path(url, OPENALEX_WORKS_ROOT)
            remote_files.append(RemoteFile(url=url, relative_path=rel_path, size_bytes=size_bytes))
    else:
        print(f"Discovered {len(remote_files)} files via S3 listing")

    total_listed = sum(f.size_bytes or 0 for f in remote_files)
    print(f"Total listed size (known): {human_bytes(total_listed)} across {len(remote_files)} files")

    # Skip existing files (size match) and compute remaining candidates
    remaining: List[RemoteFile] = []
    skipped_existing = 0
    existing_bytes = 0
    for rf in remote_files:
        dest_path = dest_root / rf.relative_path
        if dest_path.exists() and rf.size_bytes is not None and dest_path.stat().st_size == rf.size_bytes:
            skipped_existing += 1
            existing_bytes += rf.size_bytes
            continue
        remaining.append(rf)

    print(
        f"Existing matched files: {skipped_existing} ({human_bytes(existing_bytes)}), remaining candidates: {len(remaining)}"
    )

    # Enforce budget and free-space constraints
    budget_bytes = int(args.max_gib * (1024 ** 3))
    reserve_bytes = int(args.reserve_free_gib * (1024 ** 3))

    if args.dry_run:
        print("Dry-run: manifest only")
        if not args.no_manifest:
            manifest_path = dest_root.parent.parent / "manifests" / "openalex_works_manifest.json"
            write_manifest(manifest_path, remote_files, 0, skipped_existing)
        return 0

    # Download loop with a thread pool, stopping when limits are reached
    downloaded_total = 0
    downloaded_count = 0

    lock = threading.Lock()

    def should_continue(next_size: Optional[int]) -> bool:
        # Check free space and budget before scheduling a next file
        free_bytes = get_free_space_bytes(dest_root)
        if free_bytes <= reserve_bytes:
            return False
        if next_size is None:
            return True
        with lock:
            return (downloaded_total + next_size) <= budget_bytes

    # Sort by path for deterministic ordering
    remaining_sorted = sorted(remaining, key=lambda x: x.relative_path)

    print(f"Starting downloads with concurrency={args.concurrency}, budget={human_bytes(budget_bytes)}, reserve={human_bytes(reserve_bytes)}")
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures: List[concurrent.futures.Future] = []

        for item in remaining_sorted:
            if not should_continue(item.size_bytes):
                break
            futures.append(
                pool.submit(
                    download_one,
                    session,
                    item,
                    dest_root,
                    prefer_s3_download=bool(args.prefer_s3),
                )
            )

        for fut in concurrent.futures.as_completed(futures):
            try:
                rel_path, bytes_downloaded, skipped = fut.result()
            except Exception as e:
                print(f"ERROR: {e}")
                continue
            with lock:
                downloaded_total += bytes_downloaded
                if not skipped:
                    downloaded_count += 1
            status = "skipped" if skipped else f"{human_bytes(bytes_downloaded)}"
            print(f"{rel_path} -> {status}")

    print(
        f"Downloaded {downloaded_count} files totaling {human_bytes(downloaded_total)} (existing: {human_bytes(existing_bytes)})"
    )

    if not args.no_manifest:
        manifest_path = dest_root.parent.parent / "manifests" / "openalex_works_manifest.json"
        write_manifest(manifest_path, remote_files, downloaded_total, skipped_existing)
        print(f"Manifest written to: {manifest_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())


