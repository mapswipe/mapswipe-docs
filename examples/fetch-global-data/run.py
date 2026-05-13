#!/usr/bin/env python3

# See ./README.md

import argparse
import gzip
import json
import sys
import urllib.request
from http.cookiejar import CookieJar
from pathlib import Path

BASE_URL = "https://backend.mapswipe.org"
CSRFTOKEN_KEY = "MAPSWIPE-PROD-CSRFTOKEN"
REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUT = REPO_ROOT / "assets" / "docs" / "about_data" / "files" / "global"
TIMEOUT = 60

QUERY = """
    query GlobalExports {
      globalExportAssets {
        type
        lastUpdatedAt
        fileSize
        file { url name }
      }
    }
"""


def build_opener() -> tuple[urllib.request.OpenerDirector, CookieJar]:
    jar = CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
    return opener, jar


def get_csrf_token(opener: urllib.request.OpenerDirector, jar: CookieJar) -> str:
    with opener.open(f"{BASE_URL}/health-check/", timeout=TIMEOUT) as resp:
        resp.read()
    for cookie in jar:
        if cookie.name == CSRFTOKEN_KEY and cookie.value is not None:
            return cookie.value
    raise RuntimeError(f"CSRF cookie {CSRFTOKEN_KEY!r} not set by health-check")


def fetch_global_exports(opener: urllib.request.OpenerDirector, csrf_token: str) -> list[dict]:
    payload = json.dumps(
        {
            "operationName": "GlobalExports",
            "query": QUERY,
            "variables": {},
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/graphql/",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-CSRFToken": csrf_token,
            "Referer": BASE_URL + "/",
        },
        method="POST",
    )
    with opener.open(req, timeout=TIMEOUT) as resp:
        body = json.loads(resp.read())
    if "errors" in body:
        raise RuntimeError(f"GraphQL errors: {body['errors']}")
    assets = body.get("data", {}).get("globalExportAssets") or []
    if not assets:
        raise RuntimeError("globalExportAssets returned no assets")
    return assets


def maybe_decompress(payload: bytes, filename: str) -> tuple[bytes, str]:
    if filename.endswith(".gz"):
        return gzip.decompress(payload), filename[:-3]
    if payload[:2] == b"\x1f\x8b":
        return gzip.decompress(payload), filename
    return payload, filename


def sample_csv(payload: bytes, n: int) -> bytes:
    lines = payload.decode("utf-8", errors="replace").splitlines(keepends=True)
    if not lines:
        return payload
    header, *rest = lines
    return ("".join([header] + rest[:n])).encode("utf-8")


def sample_geojson(payload: bytes, n: int) -> bytes:
    try:
        obj = json.loads(payload)
    except json.JSONDecodeError:
        return payload
    if isinstance(obj, dict) and isinstance(obj.get("features"), list):
        obj["features"] = obj["features"][:n]
    return json.dumps(obj, indent=2).encode("utf-8")


def process(
    opener: urllib.request.OpenerDirector,
    url: str,
    name: str,
    out_dir: Path,
    sample: int | None,
) -> Path:
    with opener.open(url, timeout=TIMEOUT) as resp:
        raw = resp.read()
    payload, out_name = maybe_decompress(raw, name)
    if sample is not None:
        lower = out_name.lower()
        if lower.endswith(".csv"):
            payload = sample_csv(payload, sample)
        elif lower.endswith((".geojson", ".json")):
            payload = sample_geojson(payload, sample)
    out_path = out_dir / Path(out_name).name
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(payload)
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fetch MapSwipe global data exports via the GraphQL backend.",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=DEFAULT_OUT,
        help=f"Output directory (default: {DEFAULT_OUT})",
    )
    parser.add_argument(
        "--sample",
        type=int,
        default=None,
        help="If set, keep only the first N records per CSV / GeoJSON file. "
             "Default: download files in full.",
    )
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)

    opener, jar = build_opener()

    print("Acquiring CSRF token...", file=sys.stderr)
    csrf_token = get_csrf_token(opener, jar)

    print("Fetching global exports...", file=sys.stderr)
    assets = fetch_global_exports(opener, csrf_token)

    downloads: list[tuple[str, str]] = []
    for asset in assets:
        file_info = asset.get("file") or {}
        url, name = file_info.get("url"), file_info.get("name")
        if url and name:
            downloads.append((url, name))

    if not downloads:
        print("No downloadable files in response.", file=sys.stderr)
        return 1

    mode = (
        f"sampling up to {args.sample} record(s) per file"
        if args.sample is not None
        else "downloading in full"
    )
    print(f"{len(downloads)} export(s) found, {mode}.", file=sys.stderr)
    failures = 0
    for url, name in downloads:
        try:
            out_path = process(opener, url, name, args.out, args.sample)
        except Exception as exc:
            failures += 1
            print(f"  failed {name}: {exc}", file=sys.stderr)
            continue
        try:
            display = out_path.resolve().relative_to(REPO_ROOT)
        except ValueError:
            display = out_path
        print(f"  saved {display}")

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
