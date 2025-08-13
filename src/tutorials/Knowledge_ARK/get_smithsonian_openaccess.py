#!/usr/bin/env python3
"""
Smithsonian Open Access fetcher (Python)

Uses the Smithsonian Open Access API to query items (e.g., by date range,
media type, keywords) and downloads available open media (IIIF/full images,
JSON metadata) within a size budget, with concurrency, resume, and manifest.

API docs: https://www.si.edu/openaccess
Base:     https://api.si.edu/openaccess/api/v1.0

You need an API key (free). Set env SMITHSONIAN_API_KEY or pass --api-key.

Default destination:
  <repo_root>/alden-core/data/archive/smithsonian/<YYYYMMDD>/raw
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
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


API_BASE = "https://api.si.edu/openaccess/api/v1.0"


@dataclass(frozen=True)
class MediaItem:
    id: str
    media_url: str
    media_type: str
    size_bytes: Optional[int]
    metadata_json: Dict

    @property
    def filename(self) -> str:
        # Create a stable path id/<basename>
        basename = self.media_url.rstrip("/").split("/")[-1]
        if not basename:
            basename = "media"
        return f"{self.id}/{basename}"


def create_session(timeout: int = 30) -> requests.Session:
    s = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=0.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retries, pool_connections=32, pool_maxsize=32)
    s.mount("http://", adapter)
    s.mount("https://", adapter)
    s.headers.update({"User-Agent": "mindgardenai-smithsonian-fetcher/1.0"})
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


def api_search(session: requests.Session, api_key: str, query: str, rows: int = 1000, start: int = 0) -> Dict:
    params = {
        "api_key": api_key,
        "q": query,
        "rows": rows,
        "start": start,
    }
    r = session.get(f"{API_BASE}/search", params=params)
    r.raise_for_status()
    return r.json()


def enumerate_items(session: requests.Session, api_key: str, query: str, max_items: Optional[int] = None) -> List[Dict]:
    items: List[Dict] = []
    start = 0
    rows = 1000
    while True:
        data = api_search(session, api_key, query, rows=rows, start=start)
        docs = data.get("response", {}).get("rows", []) or data.get("response", {}).get("docs", [])
        if not docs:
            break
        items.extend(docs)
        start += len(docs)
        print(f"Enumerated {len(items)} items...")
        if max_items and len(items) >= max_items:
            items = items[:max_items]
            break
        if len(docs) < rows:
            break
    return items


def extract_media(doc: Dict) -> List[MediaItem]:
    out: List[MediaItem] = []
    doc_id = doc.get("id") or doc.get("_id") or doc.get("content", {}).get("descriptiveNonRepeating", {}).get("record_ID") or "item"
    media_list = []
    # Typical path: content.freetext.online_media.media
    content = doc.get("content") or {}
    freetext = content.get("freetext") or {}
    online_media = freetext.get("online_media") or {}
    media_list = online_media.get("media") or []
    for m in media_list:
        url = m.get("content") or m.get("resources", [{}])[0].get("url")
        if not url:
            continue
        mtype = m.get("type") or m.get("mediaType") or "media"
        out.append(MediaItem(id=str(doc_id), media_url=url, media_type=str(mtype), size_bytes=None, metadata_json=doc))
    return out


def download_binary(session: requests.Session, url: str, dest: Path) -> int:
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


def download_one(session: requests.Session, item: MediaItem, dest_root: Path) -> Tuple[str, int, bool]:
    dest = dest_root / item.filename
    ensure_parent(dest)
    if dest.exists() and item.size_bytes is not None:
        try:
            if dest.stat().st_size == item.size_bytes:
                return item.filename, 0, True
        except Exception:
            pass
    print(f"START {item.filename} ({item.media_type})", flush=True)
    bytes_dl = download_binary(session, item.media_url, dest)
    print(f"DONE {item.filename}: {human_bytes(bytes_dl)}", flush=True)
    # Also write metadata JSON next to the media
    meta_path = dest.with_suffix(dest.suffix + ".json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(item.metadata_json, f, indent=2)
    return item.filename, bytes_dl, False


def write_manifest(path: Path, query: str, items: List[MediaItem], downloaded_bytes: int, skipped_count: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "api_base": API_BASE,
        "query": query,
        "created_at": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "counts": {
            "total_media_listed": len(items),
            "total_bytes_listed": int(sum(i.size_bytes or 0 for i in items)),
            "downloaded_bytes": int(downloaded_bytes),
            "skipped_existing": int(skipped_count),
        },
        "media": [asdict(i) for i in items],
    }
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Fetch Smithsonian Open Access media within a size budget")
    ap.add_argument("--api-key", type=str, default=os.environ.get("SMITHSONIAN_API_KEY"), help="API key")
    ap.add_argument(
        "--query",
        type=str,
        default="online_media_type:Images AND online_media:yes",
        help="Search query (Lucene syntax)",
    )
    ap.add_argument("--max-items", type=int, default=5000, help="Max records to enumerate")
    ap.add_argument("--max-gib", type=float, default=200.0, help="Max new bytes to download")
    ap.add_argument("--reserve-free-gib", type=float, default=20.0, help="Free space to leave")
    ap.add_argument("--concurrency", type=int, default=8, help="Concurrent downloads")
    ap.add_argument("--dest-root", type=Path, default=None, help="Destination root directory")
    ap.add_argument("--dry-run", action="store_true", help="List only; no downloads")
    ap.add_argument("--no-manifest", action="store_true", help="Skip writing manifest")

    args = ap.parse_args(argv)

    if not args.api_key:
        print("ERROR: Provide Smithsonian API key via --api-key or SMITHSONIAN_API_KEY env.")
        return 2

    if args.dest_root is None:
        repo_root = Path(__file__).resolve().parents[2]
        date_str = dt.datetime.utcnow().strftime("%Y%m%d")
        args.dest_root = repo_root / "alden-core" / "data" / "archive" / "smithsonian" / date_str / "raw"
    dest: Path = args.dest_root
    dest.mkdir(parents=True, exist_ok=True)

    session = create_session()

    # Enumerate items
    print(f"Enumerating items with query: {args.query}")
    docs = enumerate_items(session, args.api_key, args.query, max_items=args.max_items)
    if not docs:
        print("No items found for the query.")
        return 1
    media: List[MediaItem] = []
    for d in docs:
        media.extend(extract_media(d))
    if not media:
        print("No media files found for the enumerated items.")
        return 1
    print(f"Found {len(media)} media files")

    # Skip existing
    remaining: List[MediaItem] = []
    skipped_count = 0
    existing_bytes = 0
    for m in media:
        p = dest / m.filename
        if p.exists():
            # No reliable size available; treat as existing if file exists
            skipped_count += 1
        else:
            remaining.append(m)

    print(f"Existing matched: {skipped_count}; remaining: {len(remaining)}")

    budget_bytes = int(args.max_gib * (1024 ** 3))
    reserve_bytes = int(args.reserve_free_gib * (1024 ** 3))
    if args.dry_run:
        if not args.no_manifest:
            manifest_path = dest.parent / "manifests" / "smithsonian_manifest.json"
            write_manifest(manifest_path, args.query, media, 0, skipped_count)
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

    remaining_sorted = sorted(remaining, key=lambda m: m.filename)
    print(
        f"Starting downloads with concurrency={args.concurrency}, budget={human_bytes(budget_bytes)}, reserve={human_bytes(reserve_bytes)}"
    )

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures: List[concurrent.futures.Future] = []
        for m in remaining_sorted:
            # No size known; schedule until free-space guard triggers during loop
            if not can_schedule(None):
                break
            futures.append(pool.submit(download_one, session, m, dest))

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
        manifest_path = dest.parent / "manifests" / "smithsonian_manifest.json"
        write_manifest(manifest_path, args.query, media, downloaded_bytes, skipped_count)
        print(f"Manifest written: {manifest_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())



