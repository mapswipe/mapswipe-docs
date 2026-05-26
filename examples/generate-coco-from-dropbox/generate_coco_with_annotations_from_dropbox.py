# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "httpx~=0.28.1",
#   "colorama",
#   "pillow",
# ]
# ///
from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import sys
import textwrap
from collections import OrderedDict
from pathlib import PurePosixPath

import httpx
from colorama import init as colorama_init, Fore

colorama_init(autoreset=True)


ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

DROPBOX_PERMISSION_MESSAGE = f"""
{Fore.YELLOW}
----------------------------------------------------
Make sure the dropbox App includes these permissions
- files.metadata.read
- files.content.write
- files.content.read
- sharing.write
- sharing.read
"""


def die(msg: str, code: int = 2) -> None:
    print(f"{Fore.RED}{msg}", file=sys.stderr)
    sys.exit(code)


def dropbox_request_error_handler(res: httpx.Response) -> None:
    try:
        res.raise_for_status()
    except httpx.HTTPStatusError as http_err:
        print(f"{Fore.RED}HTTP error occurred while requesting {res.url}: {http_err}")
        print(f"{Fore.RED}Response content: {res.text}")
        print(DROPBOX_PERMISSION_MESSAGE)
        raise
    except httpx.RequestError as req_err:
        print(
            f"{Fore.RED}An error occurred while making the request to {res.url}: {req_err}"
        )
        print(DROPBOX_PERMISSION_MESSAGE)
        raise


def dropbox_rpc(endpoint: str, data: object, *, access_token: str) -> dict:
    res = httpx.post(
        f"https://api.dropboxapi.com/2/{endpoint}",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        },
        data=json.dumps(data),
    )
    dropbox_request_error_handler(res)
    return res.json()


def dropbox_download(path: str, *, access_token: str) -> bytes:
    res = httpx.post(
        "https://content.dropboxapi.com/2/files/download",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Dropbox-API-Arg": json.dumps({"path": path}),
        },
    )
    dropbox_request_error_handler(res)
    return res.content


def dropbox_upload(path: str, content: bytes, *, access_token: str) -> dict:
    res = httpx.post(
        "https://content.dropboxapi.com/2/files/upload",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/octet-stream",
            "Dropbox-API-Arg": json.dumps(
                {
                    "path": path,
                    "mode": "overwrite",
                    "autorename": False,
                    "mute": False,
                }
            ),
        },
        content=content,
    )
    dropbox_request_error_handler(res)
    return res.json()


def list_all_files(
    folder_path: str, *, access_token: str, recursive: bool
) -> list[dict]:
    entries: list[dict] = []
    response = dropbox_rpc(
        "files/list_folder",
        {"path": folder_path, "recursive": recursive},
        access_token=access_token,
    )
    entries.extend(response.get("entries", []))
    while response.get("has_more", False):
        response = dropbox_rpc(
            "files/list_folder/continue",
            {"cursor": response["cursor"]},
            access_token=access_token,
        )
        entries.extend(response.get("entries", []))
    return entries


def collect_images(folder_path: str, *, access_token: str) -> list[dict]:
    entries = list_all_files(folder_path, access_token=access_token, recursive=True)
    images = [
        e
        for e in entries
        if e.get(".tag") == "file"
        and PurePosixPath(e["name"]).suffix.lower() in ALLOWED_EXTENSIONS
    ]
    images.sort(key=lambda e: e["path_display"].lower())
    return images


def relative_under(path_display: str, base: str) -> str:
    base_norm = base.rstrip("/").lower()
    file_norm = path_display.lower()
    prefix = base_norm + "/"
    if file_norm.startswith(prefix):
        return path_display[len(prefix):]
    if file_norm == base_norm:
        return ""
    # Fallback — shouldn't happen given Dropbox listing semantics.
    return path_display.lstrip("/")


def share_file_get_url(path: str, *, access_token: str) -> str:
    res = dropbox_rpc(
        "sharing/list_shared_links",
        {"path": path, "direct_only": True},
        access_token=access_token,
    )
    if res.get("links"):
        link = res["links"][0]["url"]
    else:
        res_create = dropbox_rpc(
            "sharing/create_shared_link_with_settings",
            {"path": path, "settings": {"requested_visibility": "public"}},
            access_token=access_token,
        )
        link = res_create["url"]
    return re.sub(r"&dl=0\b", "", link) + "&raw=1"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a COCO file with annotations from a Dropbox folder "
            "containing a CSV metadata file and an images directory."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(DROPBOX_PERMISSION_MESSAGE),
    )
    parser.add_argument(
        "base_folder",
        help='Dropbox path that contains the images folder and CSV. e.g. "/Indonesia"',
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Local path to write the COCO JSON. Default: ./<base-folder-basename>.coco.json",
    )
    parser.add_argument(
        "--images-folder",
        default="images/",
        help="Images folder, relative to base_folder (absolute Dropbox path also accepted). Default: images/",
    )
    parser.add_argument(
        "--csv-path",
        default="metadata.csv",
        help="CSV file path, relative to base_folder (absolute also accepted). Default: metadata.csv",
    )
    parser.add_argument(
        "--category-column",
        default="type",
        help="CSV column used to derive COCO categories. Default: type",
    )
    parser.add_argument(
        "--image-name-column",
        default="image_name",
        help="CSV column with the image path relative to --images-folder. Default: image_name",
    )
    parser.add_argument(
        "--boxes-column",
        default="boxes",
        help="CSV column with the bounding box (JSON-encoded 4-element list). Default: boxes",
    )
    parser.add_argument(
        "--box-format",
        choices=["xyxy", "xywh"],
        default="xyxy",
        help="Format of values in --boxes-column. xyxy is converted to COCO xywh on output. Default: xyxy",
    )
    parser.add_argument(
        "--annotation-id-column",
        default=None,
        help="CSV column to use as annotation id (must be unique). Default: sequential 1..N",
    )
    parser.add_argument(
        "--image-id-column",
        default=None,
        help="CSV column to use as image id (must be consistent per image). Default: sequential 1..N",
    )
    parser.add_argument(
        "--include-empty-images",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Include images in images[] even when they have no CSV row. Default: include",
    )
    strictness = parser.add_mutually_exclusive_group()
    strictness.add_argument(
        "--strict",
        dest="strict",
        action="store_true",
        help="(default) Hard-error on CSV rows referencing missing images.",
    )
    strictness.add_argument(
        "--lenient",
        dest="strict",
        action="store_false",
        help="Skip-and-warn on CSV rows referencing missing images.",
    )
    parser.set_defaults(strict=True)
    parser.add_argument(
        "--probe-dimensions",
        action="store_true",
        help="Download each image and probe width/height with Pillow.",
    )
    parser.add_argument(
        "--upload-to-dropbox",
        action="store_true",
        help="Also upload the COCO JSON to <base_folder>/<output basename> in Dropbox.",
    )
    return parser.parse_args()


def resolve_dbx_path(base_folder: str, sub: str) -> str:
    # If sub is an absolute Dropbox path, return as-is; otherwise join under base.
    if sub.startswith("/"):
        return str(PurePosixPath(sub))
    return str(PurePosixPath(base_folder) / sub)


def coerce_id(raw: str) -> int | str:
    raw = raw.strip()
    if raw.lstrip("-").isdigit():
        return int(raw)
    return raw


def main() -> None:
    args = parse_args()

    access_token = os.environ.get("DROPBOX_ACCESS_TOKEN")
    if not access_token:
        die("DROPBOX_ACCESS_TOKEN env var is not set.")

    base_folder = args.base_folder.rstrip("/") or "/"
    images_folder_dbx = resolve_dbx_path(base_folder, args.images_folder).rstrip("/")
    csv_path_dbx = resolve_dbx_path(base_folder, args.csv_path)

    output_path = (
        args.output
        or f"./{PurePosixPath(base_folder).name or 'coco'}.coco.json"
    )

    # 1. List images
    print(f"Listing images under {images_folder_dbx} ...")
    file_entries = collect_images(images_folder_dbx, access_token=access_token)
    print(f"  {len(file_entries)} image(s) found")

    image_by_relpath: dict[str, dict] = OrderedDict()
    for entry in file_entries:
        rel = relative_under(entry["path_display"], images_folder_dbx)
        if not rel:
            continue
        if rel in image_by_relpath:
            die(f"Duplicate relative path {rel!r} under {images_folder_dbx}.")
        image_by_relpath[rel] = entry

    # 2. Download CSV
    print(f"Downloading CSV from {csv_path_dbx} ...")
    csv_bytes = dropbox_download(csv_path_dbx, access_token=access_token)
    csv_reader = csv.DictReader(io.StringIO(csv_bytes.decode("utf-8-sig")))
    rows = list(csv_reader)
    headers = list(csv_reader.fieldnames or [])
    print(f"  {len(rows)} CSV row(s); columns: {headers}")

    required_cols = {
        args.image_name_column,
        args.boxes_column,
        args.category_column,
    }
    if args.annotation_id_column:
        required_cols.add(args.annotation_id_column)
    if args.image_id_column:
        required_cols.add(args.image_id_column)
    missing = required_cols - set(headers)
    if missing:
        die(f"CSV is missing required columns: {sorted(missing)}")

    # 3. Validate image references
    unmatched: list[tuple[int, str]] = []
    for row_idx, row in enumerate(rows, start=1):
        name = (row.get(args.image_name_column) or "").strip()
        if name not in image_by_relpath:
            unmatched.append((row_idx, name))
    if unmatched:
        preview = "\n".join(f"  row {idx}: {name!r}" for idx, name in unmatched[:20])
        more = (
            f"\n  ... ({len(unmatched) - 20} more)" if len(unmatched) > 20 else ""
        )
        msg = (
            f"{len(unmatched)} CSV row(s) reference images not found under "
            f"{images_folder_dbx}:\n{preview}{more}"
        )
        if args.strict:
            die(
                f"{msg}\nAborting (--strict). Re-run with --lenient to skip these rows."
            )
        print(f"{Fore.YELLOW}WARNING: {msg}")
        skip = {n for _, n in unmatched}
        rows = [
            r for r in rows if (r.get(args.image_name_column) or "").strip() not in skip
        ]

    # 4. Build categories[] (id by order of first appearance).
    # Empty values are routed to an "unknown" category, added on first occurrence.
    UNKNOWN_NAME = "unknown"
    categories: list[dict] = []
    cat_id_by_name: dict[str, int] = {}
    unknown_count = 0
    for row in rows:
        raw = (row.get(args.category_column) or "").strip()
        name = raw or UNKNOWN_NAME
        if not raw:
            unknown_count += 1
        if name not in cat_id_by_name:
            cat_id_by_name[name] = len(categories) + 1
            categories.append({"id": cat_id_by_name[name], "name": name})
    if unknown_count:
        print(
            f"{Fore.YELLOW}WARNING: {unknown_count} row(s) had empty "
            f"{args.category_column!r}; routed to category {UNKNOWN_NAME!r}."
        )

    # 6. Assign image ids
    rows_by_image: dict[str, list[dict]] = {}
    for row in rows:
        rows_by_image.setdefault(row[args.image_name_column].strip(), []).append(row)

    image_id_by_relpath: dict[str, int | str] = {}
    if args.image_id_column:
        for relpath, row_list in rows_by_image.items():
            ids = {r[args.image_id_column].strip() for r in row_list}
            if len(ids) > 1:
                die(
                    f"Image {relpath!r} has inconsistent values in "
                    f"{args.image_id_column!r}: {sorted(ids)}"
                )
            image_id_by_relpath[relpath] = coerce_id(next(iter(ids)))
        used_int = [v for v in image_id_by_relpath.values() if isinstance(v, int)]
        next_id = (max(used_int) + 1) if used_int else 1
        for relpath in image_by_relpath:
            if relpath not in image_id_by_relpath:
                image_id_by_relpath[relpath] = next_id
                next_id += 1
    else:
        for idx, relpath in enumerate(image_by_relpath.keys(), start=1):
            image_id_by_relpath[relpath] = idx

    # 7. Drop empty images if not included
    if not args.include_empty_images:
        kept = {r[args.image_name_column].strip() for r in rows}
        image_by_relpath = OrderedDict(
            (rp, e) for rp, e in image_by_relpath.items() if rp in kept
        )

    # 8. Share links + optional dimension probe
    images_out: list[dict] = []
    total = len(image_by_relpath)
    for i, (relpath, entry) in enumerate(image_by_relpath.items(), start=1):
        print(f"{i}/{total} sharing {relpath}")
        url = share_file_get_url(entry["path_lower"], access_token=access_token)
        record: dict = {
            "id": image_id_by_relpath[relpath],
            "file_name": relpath,
            "coco_url": url,
        }
        if args.probe_dimensions:
            from PIL import Image  # lazy import

            img_bytes = dropbox_download(entry["path_lower"], access_token=access_token)
            with Image.open(io.BytesIO(img_bytes)) as im:
                record["width"], record["height"] = im.size
        images_out.append(record)

    # 9. Build annotations[]
    attribute_columns = [
        c
        for c in headers
        if c
        not in {
            args.image_name_column,
            args.boxes_column,
            args.category_column,
            args.annotation_id_column,
            args.image_id_column,
        }
    ]
    annotations_out: list[dict] = []
    seen_ann_ids: set = set()

    for row_idx, row in enumerate(rows, start=1):
        relpath = row[args.image_name_column].strip()
        image_id = image_id_by_relpath[relpath]

        raw_box = row[args.boxes_column]
        try:
            box = json.loads(raw_box)
        except (json.JSONDecodeError, TypeError) as exc:
            die(
                f"Row {row_idx}: failed to parse {args.boxes_column!r} as JSON: {exc}"
            )
        if not isinstance(box, list) or len(box) != 4:
            die(
                f"Row {row_idx}: {args.boxes_column!r} is not a 4-element list: "
                f"{box!r}"
            )
        if args.box_format == "xyxy":
            x1, y1, x2, y2 = box
            bbox = [x1, y1, x2 - x1, y2 - y1]
        else:
            bbox = list(box)

        if args.annotation_id_column:
            ann_id = coerce_id(row[args.annotation_id_column])
            if ann_id in seen_ann_ids:
                die(f"Row {row_idx}: duplicate annotation id {ann_id!r}")
            seen_ann_ids.add(ann_id)
        else:
            ann_id = len(annotations_out) + 1

        cat_name = (row.get(args.category_column) or "").strip() or UNKNOWN_NAME
        annotations_out.append(
            {
                "id": ann_id,
                "image_id": image_id,
                "bbox": bbox,
                "category_id": cat_id_by_name[cat_name],
                "attributes": {col: row[col] for col in attribute_columns},
            }
        )

    coco = {
        "images": images_out,
        "annotations": annotations_out,
        "categories": categories,
    }

    # 10. Write locally
    with open(output_path, "w") as f:
        json.dump(coco, f, indent=2)
    print(f"{Fore.GREEN}Wrote {output_path}")

    # 11. Optional Dropbox upload
    dropbox_link: str | None = None
    if args.upload_to_dropbox:
        out_basename = PurePosixPath(output_path).name
        dest = str(PurePosixPath(base_folder) / out_basename)
        print(f"Uploading COCO file to {dest} ...")
        dropbox_upload(
            dest, json.dumps(coco).encode("utf-8"), access_token=access_token
        )
        link_res = dropbox_rpc(
            "files/get_temporary_link", {"path": dest}, access_token=access_token
        )
        dropbox_link = link_res["link"]
        print(f"{Fore.GREEN}Uploaded to {dest}")
        print(f"{Fore.GREEN}Temporary link: {dropbox_link}")

    # 12. Summary
    images_with_detections = len(
        {r[args.image_name_column].strip() for r in rows}
        & set(image_by_relpath.keys())
    )
    print()
    print(f"{Fore.CYAN}Summary:")
    print(f"  Categories:  {len(categories)}")
    print(
        f"  Images:      {len(images_out)} ({images_with_detections} with detections)"
    )
    print(f"  Annotations: {len(annotations_out)}")
    print(f"  Output:      {output_path}")
    if dropbox_link:
        print(f"  Dropbox:     {dropbox_link}")


if __name__ == "__main__":
    main()
