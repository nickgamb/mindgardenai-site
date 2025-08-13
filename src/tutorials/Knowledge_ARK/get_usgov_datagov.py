#!/usr/bin/env python3
"""
US Gov Open Data (data.gov CKAN) fetcher (Python)

Queries the data.gov CKAN API for datasets matching a query or organization,
then downloads resource files (CSV/JSON/ZIP/etc.) within a size budget, with
concurrency, resume, and manifest.

API: https://catalog.data.gov/api/3/

Default destination:
  <repo_root>/alden-core/data/archive/data_gov/<YYYYMMDD>/raw

Examples:
  python alden-core/tools/get_usgov_datagov.py --query climate --max-gib 200 --concurrency 8
  python alden-core/tools/get_usgov_datagov.py --org usgs-gov --max-gib 200
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


CKAN_BASE = "https://catalog.data.gov/api/3"


@dataclass(frozen=True)
class Resource:
    dataset_id: str
    dataset_title: str
    url: str
    format: str
    size_bytes: Optional[int]

    @property
    def filename(self) -> str:
        # dataset_id/resource_basename
        base = self.url.split("?")[0].rstrip("/").split("/")[-1]
        return f"{self.dataset_id}/{base or 'resource'}"


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
    s.headers.update({"User-Agent": "mindgardenai-datagov-fetcher/1.0"})
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


def ckan_search(session: requests.Session, *, query: Optional[str], org: Optional[str], rows: int, start: int) -> Dict:
    params = {"rows": rows, "start": start}
    if query:
        params["q"] = query
    if org:
        params["fq"] = f"organization:{org}"
    r = session.get(f"{CKAN_BASE}/action/package_search", params=params)
    r.raise_for_status()
    return r.json()


def enumerate_resources(session: requests.Session, *, query: Optional[str], org: Optional[str], max_datasets: int) -> List[Resource]:
    start = 0
    rows = 100
    resources: List[Resource] = []
    while True:
        data = ckan_search(session, query=query, org=org, rows=rows, start=start)
        result = data.get("result", {})
        packages = result.get("results", [])
        if not packages:
            break
        for p in packages:
            ds_id = p.get("id") or "dataset"
            ds_title = p.get("title") or "dataset"
            for rsrc in p.get("resources", []) or []:
                url = rsrc.get("url") or rsrc.get("download_url")
                if not url:
                    continue
                fmt = (rsrc.get("format") or rsrc.get("mimetype") or "").lower()
                size = rsrc.get("size")
                size_int = int(size) if isinstance(size, (int, float)) else None
                resources.append(Resource(dataset_id=ds_id, dataset_title=ds_title, url=url, format=fmt, size_bytes=size_int))
        start += len(packages)
        print(f"Enumerated datasets: {start} -> resources so far: {len(resources)}")
        if start >= max_datasets or len(packages) < rows:
            break
    return resources


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


def download_one(session: requests.Session, res: Resource, dest_root: Path) -> Tuple[str, int, bool]:
    dest = dest_root / res.filename
    ensure_parent(dest)
    if dest.exists() and res.size_bytes is not None:
        try:
            if dest.stat().st_size == res.size_bytes:
                return res.filename, 0, True
        except Exception:
            pass
    print(f"START {res.filename} ({res.format})", flush=True)
    bytes_dl = download_binary(session, res.url, dest)
    print(f"DONE {res.filename}: {human_bytes(bytes_dl)}", flush=True)
    return res.filename, bytes_dl, False


def write_manifest(path: Path, meta: Dict, resources: List[Resource], downloaded_bytes: int, skipped_count: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "ckan_base": CKAN_BASE,
        "meta": meta,
        "created_at": dt.datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "counts": {
            "total_resources_listed": len(resources),
            "total_bytes_listed": int(sum(r.size_bytes or 0 for r in resources)),
            "downloaded_bytes": int(downloaded_bytes),
            "skipped_existing": int(skipped_count),
        },
        "resources": [asdict(r) for r in resources],
    }
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="Fetch US data.gov resources within a size budget")
    ap.add_argument("--query", type=str, default=None, help="Search query")
    ap.add_argument("--org", type=str, default=None, help="Organization filter (e.g., usgs-gov)")
    ap.add_argument("--max-datasets", type=int, default=500, help="Max datasets to enumerate")
    ap.add_argument("--max-gib", type=float, default=200.0, help="Max new bytes to download")
    ap.add_argument("--reserve-free-gib", type=float, default=20.0, help="Free space to leave")
    ap.add_argument("--concurrency", type=int, default=8, help="Concurrent downloads")
    ap.add_argument("--dest-root", type=Path, default=None, help="Destination root directory")
    ap.add_argument("--dry-run", action="store_true", help="List only; no downloads")
    ap.add_argument("--no-manifest", action="store_true", help="Skip writing manifest")

    args = ap.parse_args(argv)

    if args.dest_root is None:
        repo_root = Path(__file__).resolve().parents[2]
        date_str = dt.datetime.utcnow().strftime("%Y%m%d")
        args.dest_root = repo_root / "alden-core" / "data" / "archive" / "data_gov" / date_str / "raw"
    dest: Path = args.dest_root
    dest.mkdir(parents=True, exist_ok=True)

    session = create_session()

    # Enumerate resources
    resources = enumerate_resources(session, query=args.query, org=args.org, max_datasets=args.max_datasets)
    if not resources:
        print("No resources found.")
        return 1
    print(f"Found {len(resources)} resources")

    # Skip existing
    remaining: List[Resource] = []
    skipped_count = 0
    existing_bytes = 0
    for r in resources:
        p = dest / r.filename
        if p.exists() and r.size_bytes is not None and p.stat().st_size == r.size_bytes:
            skipped_count += 1
            existing_bytes += r.size_bytes
        else:
            remaining.append(r)

    print(f"Existing matched: {skipped_count} ({human_bytes(existing_bytes)}); remaining: {len(remaining)}")

    budget_bytes = int(args.max_gib * (1024 ** 3))
    reserve_bytes = int(args.reserve_free_gib * (1024 ** 3))
    if args.dry_run:
        if not args.no_manifest:
            manifest_path = dest.parent / "manifests" / "data_gov_manifest.json"
            write_manifest(manifest_path, {"query": args.query, "org": args.org}, resources, 0, skipped_count)
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

    remaining_sorted = sorted(remaining, key=lambda r: r.filename)
    print(
        f"Starting downloads with concurrency={args.concurrency}, budget={human_bytes(budget_bytes)}, reserve={human_bytes(reserve_bytes)}"
    )

    with concurrent.futures.ThreadPoolExecutor(max_workers=args.concurrency) as pool:
        futures: List[concurrent.futures.Future] = []
        for r in remaining_sorted:
            if not can_schedule(r.size_bytes):
                break
            futures.append(pool.submit(download_one, session, r, dest))

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

    print(f"Downloaded {downloaded_count} resources totaling {human_bytes(downloaded_bytes)}")
    if not args.no_manifest:
        manifest_path = dest.parent / "manifests" / "data_gov_manifest.json"
        write_manifest(manifest_path, {"query": args.query, "org": args.org}, resources, downloaded_bytes, skipped_count)
        print(f"Manifest written: {manifest_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())



