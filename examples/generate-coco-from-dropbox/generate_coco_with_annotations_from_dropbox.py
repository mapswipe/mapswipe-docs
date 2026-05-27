# /// script
# requires-python = ">=3.13"
# dependencies = [
#   "httpx~=0.28.1",
#   "colorama",
#   "pillow",
# ]
# ///
import argparse
import csv
import io
import json
import os
import sys
import textwrap
from collections import OrderedDict
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, Literal, NoReturn, Self, TypedDict, cast
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

import httpx
from colorama import Fore
from colorama import init as colorama_init
from PIL import Image

colorama_init(autoreset=True)

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
UNKNOWN_CATEGORY = "unknown"

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


# ---------------------------------------------------------------------------
# Dropbox API: typed request/response shapes
# ---------------------------------------------------------------------------

# ".tag" isn't a valid Python identifier, so use the functional TypedDict form.
# We only model the file-entry shape: callers must filter ".tag" == "file"
# before accessing the path/name fields.
FileEntry = TypedDict(
    "FileEntry",
    {
        ".tag": Literal["file", "folder", "deleted"],
        "name": str,
        "path_display": str,
        "path_lower": str,
    },
)


class ListFolderResponse(TypedDict):
    entries: list[FileEntry]
    cursor: str
    has_more: bool


class SharedLink(TypedDict):
    url: str


class ListSharedLinksResponse(TypedDict):
    links: list[SharedLink]


class CreateSharedLinkResponse(TypedDict):
    url: str


class TemporaryLinkResponse(TypedDict):
    link: str


class UploadResponse(TypedDict, total=False):
    id: str
    name: str
    path_display: str


# ---------------------------------------------------------------------------
# COCO output shapes
# ---------------------------------------------------------------------------


type CocoId = int | str


class CocoCategory(TypedDict):
    id: int
    name: str


class _CocoImageBase(TypedDict):
    id: CocoId
    file_name: str
    coco_url: str


class CocoImage(_CocoImageBase, total=False):
    width: int
    height: int


class CocoAnnotation(TypedDict):
    id: CocoId
    image_id: CocoId
    bbox: list[float]
    category_id: int
    attributes: dict[str, str]


class CocoDocument(TypedDict):
    images: list[CocoImage]
    annotations: list[CocoAnnotation]
    categories: list[CocoCategory]


# ---------------------------------------------------------------------------
# Errors
# ---------------------------------------------------------------------------


def die(msg: str, code: int = 2) -> NoReturn:
    print(f"{Fore.RED}{msg}", file=sys.stderr)
    sys.exit(code)


# ---------------------------------------------------------------------------
# Dropbox client
# ---------------------------------------------------------------------------


class DropboxClient:
    """Thin Dropbox v2 client. Reuses one HTTP connection pool."""

    API = "https://api.dropboxapi.com/2"
    CONTENT = "https://content.dropboxapi.com/2"

    def __init__(self, access_token: str) -> None:
        self._token = access_token
        self._client = httpx.Client(timeout=httpx.Timeout(60.0))

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def _raise(self, res: httpx.Response) -> None:
        try:
            res.raise_for_status()
        except httpx.HTTPStatusError as err:
            request = res.request
            body = (
                request.content.decode("utf-8", errors="replace")
                if request.content
                else ""
            )
            api_arg = request.headers.get("Dropbox-API-Arg", "")
            print(f"{Fore.RED}HTTP error occurred while requesting {res.url}: {err}")
            if body:
                print(f"{Fore.RED}Request body: {body}")
            if api_arg:
                print(f"{Fore.RED}Dropbox-API-Arg: {api_arg}")
            print(f"{Fore.RED}Response content: {res.text}")
            print(DROPBOX_PERMISSION_MESSAGE)
            raise
        except httpx.RequestError as err:
            print(
                f"{Fore.RED}An error occurred while making the request to "
                f"{res.url}: {err}"
            )
            print(DROPBOX_PERMISSION_MESSAGE)
            raise

    def _post(self, endpoint: str, data: object) -> dict:
        res = self._client.post(
            f"{self.API}/{endpoint}",
            headers={
                "Authorization": f"Bearer {self._token}",
                "Content-Type": "application/json",
            },
            content=json.dumps(data),
        )
        self._raise(res)
        return res.json()

    # -- typed wrappers --

    def _list_folder(
        self, path: PurePosixPath, *, recursive: bool
    ) -> ListFolderResponse:
        return cast(
            ListFolderResponse,
            self._post(
                "files/list_folder",
                {"path": str(path), "recursive": recursive},
            ),
        )

    def _list_folder_continue(self, cursor: str) -> ListFolderResponse:
        return cast(
            ListFolderResponse,
            self._post("files/list_folder/continue", {"cursor": cursor}),
        )

    def list_all_files(
        self,
        folder: PurePosixPath,
        *,
        recursive: bool,
        sort_key: Callable[[FileEntry], Any] | None = None,
    ) -> list[FileEntry]:
        entries: list[FileEntry] = []
        response = self._list_folder(folder, recursive=recursive)
        entries.extend(response.get("entries", []))
        while response.get("has_more", False):
            response = self._list_folder_continue(response["cursor"])
            entries.extend(response.get("entries", []))
        if sort_key is not None:
            entries.sort(key=sort_key)
        return entries

    def list_all_images(
        self,
        folder: PurePosixPath,
        *,
        recursive: bool = True,
        sort_key: Callable[[FileEntry], Any] | None = None,
    ) -> list[FileEntry]:
        entries = self.list_all_files(folder, recursive=recursive)
        images = [
            e
            for e in entries
            if e.get(".tag") == "file"
            and PurePosixPath(e["name"]).suffix.lower() in ALLOWED_EXTENSIONS
        ]
        if sort_key is not None:
            images.sort(key=sort_key)
        return images

    def list_shared_links(self, path: PurePosixPath) -> ListSharedLinksResponse:
        return cast(
            ListSharedLinksResponse,
            self._post(
                "sharing/list_shared_links",
                {"path": str(path), "direct_only": True},
            ),
        )

    def create_shared_link(self, path: PurePosixPath) -> CreateSharedLinkResponse:
        return cast(
            CreateSharedLinkResponse,
            self._post(
                "sharing/create_shared_link_with_settings",
                {"path": str(path), "settings": {"requested_visibility": "public"}},
            ),
        )

    def get_temporary_link(self, path: PurePosixPath) -> TemporaryLinkResponse:
        return cast(
            TemporaryLinkResponse,
            self._post("files/get_temporary_link", {"path": str(path)}),
        )

    def download(self, path: PurePosixPath) -> bytes:
        res = self._client.post(
            f"{self.CONTENT}/files/download",
            headers={
                "Authorization": f"Bearer {self._token}",
                "Dropbox-API-Arg": json.dumps({"path": str(path)}),
            },
        )
        self._raise(res)
        return res.content

    def upload(self, path: PurePosixPath, content: bytes) -> UploadResponse:
        res = self._client.post(
            f"{self.CONTENT}/files/upload",
            headers={
                "Authorization": f"Bearer {self._token}",
                "Content-Type": "application/octet-stream",
                "Dropbox-API-Arg": json.dumps(
                    {
                        "path": str(path),
                        "mode": "overwrite",
                        "autorename": False,
                        "mute": False,
                    }
                ),
            },
            content=content,
        )
        self._raise(res)
        return cast(UploadResponse, res.json())

    @staticmethod
    def to_raw_url(url: str) -> str:
        """Convert a Dropbox preview URL to a direct-content URL (raw=1)."""
        parts = urlsplit(url)
        query = [
            (k, v)
            for k, v in parse_qsl(parts.query, keep_blank_values=True)
            if k != "dl"
        ]
        query.append(("raw", "1"))
        return urlunsplit(parts._replace(query=urlencode(query)))

    def get_or_create_shareable_url(self, path: PurePosixPath) -> str:
        """Return a raw shared URL for `path`, creating the share link if needed."""
        res = self.list_shared_links(path)
        links = res.get("links") or []
        if links:
            url = links[0]["url"]
        else:
            url = self.create_shared_link(path)["url"]
        return self.to_raw_url(url)


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------


def resolve_path(base_folder: PurePosixPath, sub: str) -> PurePosixPath:
    """Join `sub` under `base_folder`, unless `sub` is already absolute."""
    p = PurePosixPath(sub)
    return p if p.is_absolute() else base_folder / sub


# ---------------------------------------------------------------------------
# Args
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Args:
    base_folder: PurePosixPath
    output_path: Path
    images_path_dropbox: PurePosixPath
    metadata_csv_path_dropbox: PurePosixPath
    category_column: str
    image_name_column: str
    boxes_column: str
    box_format: Literal["xyxy", "xywh"]
    annotation_id_column: str | None
    image_id_column: str | None
    is_strict: bool
    should_probe_dimensions: bool
    should_upload_to_dropbox: bool


def parse_args() -> Args:
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
        "--images-path",
        default="images/",
        help="Images folder, relative to base_folder (absolute Dropbox path also accepted). Default: images/",
    )
    parser.add_argument(
        "--metadata-csv-path",
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
        help="CSV column with the image path relative to --images-path. Default: image_name",
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
    ns = parser.parse_args()

    base_folder = PurePosixPath(ns.base_folder.rstrip("/") or "/")
    images_path_dropbox = resolve_path(base_folder, ns.images_path)
    metadata_csv_path_dropbox = resolve_path(base_folder, ns.metadata_csv_path)
    output_path = Path(
        ns.output or f"./{base_folder.name or 'untitled'}.coco.json"
    )

    return Args(
        base_folder=base_folder,
        output_path=output_path,
        images_path_dropbox=images_path_dropbox,
        metadata_csv_path_dropbox=metadata_csv_path_dropbox,
        category_column=ns.category_column,
        image_name_column=ns.image_name_column,
        boxes_column=ns.boxes_column,
        box_format=ns.box_format,
        annotation_id_column=ns.annotation_id_column,
        image_id_column=ns.image_id_column,
        is_strict=ns.strict,
        should_probe_dimensions=ns.probe_dimensions,
        should_upload_to_dropbox=ns.upload_to_dropbox,
    )


# ---------------------------------------------------------------------------
# Dropbox-side loaders / writers
# ---------------------------------------------------------------------------


def list_dropbox_image_index(
    client: DropboxClient,
    folder: PurePosixPath,
    base_folder: PurePosixPath,
) -> dict[PurePosixPath, FileEntry]:
    """List images under `folder`, keyed by their path relative to `base_folder`."""
    print(f"Listing images under {folder} ...")
    file_entries = client.list_all_images(
        folder, sort_key=lambda e: e["path_display"].lower()
    )
    print(f"  {len(file_entries)} image(s) found")

    base_depth = len(base_folder.parts)
    index: dict[PurePosixPath, FileEntry] = OrderedDict()
    for entry in file_entries:
        rel = PurePosixPath(
            *PurePosixPath(entry["path_display"]).parts[base_depth:]
        )
        if rel in index:
            die(f"Duplicate relative path {str(rel)!r} under {base_folder}.")
        index[rel] = entry
    return index


def load_dropbox_csv_rows(
    client: DropboxClient, csv_path: PurePosixPath
) -> tuple[list[dict[str, str]], list[str]]:
    """Download a CSV from Dropbox and parse it into row dicts + headers.

    Every field is normalised to a stripped string — never None — so callers
    can use plain `row[col]` access without further defensive shaping.
    """
    print(f"Downloading CSV from {csv_path} ...")
    csv_bytes = client.download(csv_path)
    reader = csv.DictReader(io.StringIO(csv_bytes.decode("utf-8-sig")))
    rows = [{k: (v or "").strip() for k, v in row.items()} for row in reader]
    headers = list(reader.fieldnames or [])
    print(f"  {len(rows)} CSV row(s); columns: {headers}")
    return rows, headers


def write_output(coco: CocoDocument, output_path: Path) -> None:
    with output_path.open("w") as f:
        json.dump(coco, f, indent=2)
    print(f"{Fore.GREEN}Wrote {output_path}")


def upload_coco_to_dropbox(
    client: DropboxClient,
    coco: CocoDocument,
    base_folder: PurePosixPath,
    output_path: Path,
) -> str:
    dest = base_folder / output_path.name
    print(f"Uploading COCO file to {dest} ...")
    client.upload(dest, json.dumps(coco).encode("utf-8"))
    link = client.get_temporary_link(dest)["link"]
    print(f"{Fore.GREEN}Uploaded to {dest}")
    print(f"{Fore.GREEN}Temporary link: {link}")
    return link


# ---------------------------------------------------------------------------
# CocoBuilder (pure: no CSV / Dropbox knowledge)
# ---------------------------------------------------------------------------


def coerce_id(raw: str) -> CocoId:
    # Only integer-looking strings coerce; "1.0" stays as the string "1.0".
    raw = raw.strip()
    if raw.lstrip("-").isdigit():
        return int(raw)
    return raw


@dataclass(frozen=True)
class BuilderOptions:
    """Column mappings and output toggles consumed by CocoBuilder."""

    category_column: str
    image_name_column: str
    boxes_column: str
    box_format: Literal["xyxy", "xywh"]
    annotation_id_column: str | None
    image_id_column: str | None
    is_strict: bool

    @classmethod
    def from_args(cls, args: Args) -> Self:
        return cls(
            category_column=args.category_column,
            image_name_column=args.image_name_column,
            boxes_column=args.boxes_column,
            box_format=args.box_format,
            annotation_id_column=args.annotation_id_column,
            image_id_column=args.image_id_column,
            is_strict=args.is_strict,
        )


def ensure_required_fields(fields: list[str], args: Args) -> None:
    """Hard-error if `fields` is missing any field referenced by `args`."""
    required = {
        args.image_name_column,
        args.boxes_column,
        args.category_column,
    }
    if args.annotation_id_column:
        required.add(args.annotation_id_column)
    if args.image_id_column:
        required.add(args.image_id_column)
    missing = required - set(fields)
    if missing:
        die(f"Input is missing required fields: {sorted(missing)}")


@dataclass
class _Item:
    """An input row plus per-item state set during validation."""

    fields: dict[str, str]
    skipped: bool = False
    # COCO-format (xywh) bbox; populated by `validate_bboxes` for non-skipped items.
    parsed_bbox: list[float] = field(default_factory=list)
    # Populated by `validate_annotation_ids` for non-skipped items.
    annotation_id: CocoId | None = None


class CocoBuilder:
    """Build a COCO document from in-memory items + an image relative_path set.

    The builder is agnostic to data sources. Callers provide:
      - `items` / `fields`: item dicts and the set of field names (typically
        CSV rows + headers, but any dict-shape works)
      - `image_relative_paths`: relative paths of known images (typically from
        a listing)
      - `resolve_image_url(relative_path) -> str`: returns the COCO url for an
        image
      - `probe_image_dimensions(relative_path) -> (w, h)`: optional; enables
        width/height
      - `image_source_label`: human-readable label for error messages
    """

    def __init__(
        self,
        *,
        options: BuilderOptions,
        items: list[dict[str, str]],
        fields: list[str],
        image_relative_paths: Iterable[PurePosixPath],
        resolve_image_url: Callable[[PurePosixPath], str],
        probe_image_dimensions: Callable[[PurePosixPath], tuple[int, int]]
        | None = None,
        image_source_label: str,
    ) -> None:
        self._options = options
        # Items keep their original 1-based position; the `skipped` flag is
        # set during validation, so item_idx in errors always refers to the
        # original input position.
        self._items: list[_Item] = [_Item(fields=item) for item in items]
        self._fields = list(fields)
        # Dict-as-ordered-set: keeps listing order, gives O(1) membership.
        self._image_relative_paths: dict[PurePosixPath, None] = dict.fromkeys(
            image_relative_paths
        )
        self._resolve_image_url = resolve_image_url
        self._probe_image_dimensions = probe_image_dimensions
        self._image_source_label = image_source_label

    def validate_image_references(self) -> None:
        """Flag items whose image_name has no matching image (or hard-error in strict)."""
        opts = self._options
        unmatched: list[tuple[int, str]] = []
        for item_idx, item in enumerate(self._items, start=1):
            if item.skipped:
                continue
            name = item.fields[opts.image_name_column]
            if not name:
                item.skipped = True
            elif PurePosixPath(name) not in self._image_relative_paths:
                unmatched.append((item_idx, name))
                item.skipped = True
        if not unmatched:
            return

        preview = "\n".join(f"  item {idx}: {name!r}" for idx, name in unmatched[:20])
        more = (
            f"\n  ... ({len(unmatched) - 20} more)" if len(unmatched) > 20 else ""
        )
        msg = (
            f"{len(unmatched)} item(s) reference images not found in "
            f"{self._image_source_label}:\n{preview}{more}"
        )
        if opts.is_strict:
            die(
                f"{msg}\nAborting (--strict). Re-run with --lenient to skip these items."
            )
        print(f"{Fore.YELLOW}WARNING: {msg}")

    def build_categories(self) -> tuple[list[CocoCategory], dict[str, int]]:
        category_column = self._options.category_column
        categories: list[CocoCategory] = []
        category_id_by_name: dict[str, int] = {}
        unknown_count = 0
        for item in self._items:
            if item.skipped:
                continue
            raw = item.fields[category_column]
            name = raw or UNKNOWN_CATEGORY
            if not raw:
                unknown_count += 1
            if name not in category_id_by_name:
                category_id_by_name[name] = len(categories) + 1
                categories.append({"id": category_id_by_name[name], "name": name})
        if unknown_count:
            print(
                f"{Fore.YELLOW}WARNING: {unknown_count} item(s) had empty "
                f"{category_column!r}; routed to category {UNKNOWN_CATEGORY!r}."
            )
        return categories, category_id_by_name

    def validate_bboxes(self) -> None:
        """Parse + convert each item's bbox; flag invalid ones (or hard-error in strict)."""
        opts = self._options
        invalid: list[tuple[int, str]] = []
        for item_idx, item in enumerate(self._items, start=1):
            if item.skipped:
                continue
            raw_box = item.fields[opts.boxes_column]
            try:
                box = json.loads(raw_box)
            except (json.JSONDecodeError, TypeError) as exc:
                invalid.append((item_idx, f"failed to parse as JSON: {exc}"))
                item.skipped = True
                continue
            if not isinstance(box, list) or len(box) != 4:
                invalid.append((item_idx, f"not a 4-element list: {box!r}"))
                item.skipped = True
                continue
            if opts.box_format == "xyxy":
                x1, y1, x2, y2 = box
                item.parsed_bbox = [x1, y1, x2 - x1, y2 - y1]
            else:
                item.parsed_bbox = list(box)
        if not invalid:
            return

        preview = "\n".join(
            f"  item {idx}: {opts.boxes_column!r} {err}"
            for idx, err in invalid[:20]
        )
        more = (
            f"\n  ... ({len(invalid) - 20} more)" if len(invalid) > 20 else ""
        )
        msg = (
            f"{len(invalid)} item(s) have invalid {opts.boxes_column!r}:\n"
            f"{preview}{more}"
        )
        if opts.is_strict:
            die(
                f"{msg}\nAborting (--strict). Re-run with --lenient to skip invalid items."
            )
        print(f"{Fore.YELLOW}WARNING: {msg}")

    def assign_image_ids(self) -> dict[PurePosixPath, CocoId]:
        opts = self._options
        image_id_by_path: dict[PurePosixPath, CocoId] = {}

        if not opts.image_id_column:
            # Group items by image_name and assign 1..N to each unique image
            # in order of first appearance. We deliberately walk every item
            # (including skipped ones) so an image's id is stable regardless
            # of which items happen to be skipped on a given run.
            next_id = 1
            for item in self._items:
                path = PurePosixPath(item.fields[opts.image_name_column])
                if path not in image_id_by_path:
                    image_id_by_path[path] = next_id
                    next_id += 1
            return image_id_by_path

        # Many items may share an image; all such items must declare the same
        # image_id, and no two distinct images may claim the same id.
        path_by_id: dict[CocoId, PurePosixPath] = {}
        inconsistent: list[tuple[int, str, CocoId, CocoId]] = []
        reused_id: list[tuple[int, CocoId, str, str]] = []
        for item_idx, item in enumerate(self._items, start=1):
            if item.skipped:
                continue
            path = PurePosixPath(item.fields[opts.image_name_column])
            new_id = coerce_id(item.fields[opts.image_id_column])

            existing_id = image_id_by_path.get(path)
            if existing_id is not None:
                if existing_id != new_id:
                    inconsistent.append((item_idx, str(path), new_id, existing_id))
                    item.skipped = True
                continue  # path already mapped; consistent items just share it

            existing_path = path_by_id.get(new_id)
            if existing_path is not None:
                reused_id.append((item_idx, new_id, str(path), str(existing_path)))
                item.skipped = True
                continue

            image_id_by_path[path] = new_id
            path_by_id[new_id] = path

        if inconsistent:
            preview = "\n".join(
                f"  item {idx}: {p!r} declares {opts.image_id_column!r}={n!r}, "
                f"but {e!r} was established earlier"
                for idx, p, n, e in inconsistent[:20]
            )
            more = (
                f"\n  ... ({len(inconsistent) - 20} more)"
                if len(inconsistent) > 20
                else ""
            )
            msg = (
                f"{len(inconsistent)} item(s) declare an {opts.image_id_column!r} "
                f"inconsistent with an earlier item for the same image:\n{preview}{more}"
            )
            if opts.is_strict:
                die(
                    f"{msg}\nAborting (--strict). Re-run with --lenient to skip these items."
                )
            print(f"{Fore.YELLOW}WARNING: {msg}")

        if reused_id:
            preview = "\n".join(
                f"  item {idx}: {opts.image_id_column!r} {i!r} "
                f"(already used by {ep!r}, claimed by {p!r})"
                for idx, i, p, ep in reused_id[:20]
            )
            more = (
                f"\n  ... ({len(reused_id) - 20} more)"
                if len(reused_id) > 20
                else ""
            )
            msg = (
                f"{len(reused_id)} item(s) reuse an {opts.image_id_column!r} "
                f"already assigned to a different image:\n{preview}{more}"
            )
            if opts.is_strict:
                die(
                    f"{msg}\nAborting (--strict). Re-run with --lenient to skip these items."
                )
            print(f"{Fore.YELLOW}WARNING: {msg}")

        return image_id_by_path

    def validate_annotation_ids(self) -> None:
        """Stash annotation_id on each non-skipped item.

        If `annotation_id_column` is set, parse + dedup; otherwise auto-assign
        each non-skipped item its 1-based item position so ids are stable
        across runs (skipped positions leave gaps in the output).
        """
        opts = self._options
        if not opts.annotation_id_column:
            for item_idx, item in enumerate(self._items, start=1):
                if item.skipped:
                    continue
                item.annotation_id = item_idx
            return

        seen: dict[CocoId, int] = {}
        duplicates: list[tuple[int, CocoId, int]] = []
        for item_idx, item in enumerate(self._items, start=1):
            if item.skipped:
                continue
            annotation_id = coerce_id(item.fields[opts.annotation_id_column])
            existing_idx = seen.get(annotation_id)
            if existing_idx is not None:
                duplicates.append((item_idx, annotation_id, existing_idx))
                item.skipped = True
                continue
            seen[annotation_id] = item_idx
            item.annotation_id = annotation_id

        if not duplicates:
            return

        preview = "\n".join(
            f"  item {idx}: {opts.annotation_id_column!r} {dup_id!r} "
            f"(already used by item {first})"
            for idx, dup_id, first in duplicates[:20]
        )
        more = (
            f"\n  ... ({len(duplicates) - 20} more)" if len(duplicates) > 20 else ""
        )
        msg = (
            f"{len(duplicates)} item(s) have a duplicate "
            f"{opts.annotation_id_column!r}:\n{preview}{more}"
        )
        if opts.is_strict:
            die(
                f"{msg}\nAborting (--strict). Re-run with --lenient to skip duplicates."
            )
        print(f"{Fore.YELLOW}WARNING: {msg}")

    def get_used_image_relative_paths(self) -> dict[PurePosixPath, None]:
        """Return `_image_relative_paths` filtered to images referenced by surviving items."""
        kept = {
            PurePosixPath(item.fields[self._options.image_name_column])
            for item in self._items
            if not item.skipped
        }
        return {
            relative_path: None
            for relative_path in self._image_relative_paths
            if relative_path in kept
        }

    def build_image_records(
        self,
        image_id_by_path: dict[PurePosixPath, CocoId],
        image_relative_paths: dict[PurePosixPath, None],
    ) -> list[CocoImage]:
        images: list[CocoImage] = []
        total = len(image_relative_paths)
        for idx, relative_path in enumerate(image_relative_paths, start=1):
            print(f"{idx}/{total} resolving {relative_path}")
            record: CocoImage = {
                "id": image_id_by_path[relative_path],
                "file_name": str(relative_path),
                "coco_url": self._resolve_image_url(relative_path),
            }
            if self._probe_image_dimensions is not None:
                record["width"], record["height"] = self._probe_image_dimensions(
                    relative_path
                )
            images.append(record)
        return images

    def build_annotations(
        self,
        image_id_by_path: dict[PurePosixPath, CocoId],
        category_id_by_name: dict[str, int],
    ) -> list[CocoAnnotation]:
        opts = self._options
        attribute_fields = [
            f
            for f in self._fields
            if f
            not in {
                opts.image_name_column,
                opts.boxes_column,
                opts.category_column,
                opts.annotation_id_column,
                opts.image_id_column,
            }
        ]
        annotations: list[CocoAnnotation] = []

        for item in self._items:
            if item.skipped:
                continue
            fields = item.fields
            relative_path = PurePosixPath(fields[opts.image_name_column])
            image_id = image_id_by_path[relative_path]
            annotation_id = cast(CocoId, item.annotation_id)

            category_name = fields[opts.category_column] or UNKNOWN_CATEGORY
            annotations.append(
                {
                    "id": annotation_id,
                    "image_id": image_id,
                    "bbox": item.parsed_bbox,
                    "category_id": category_id_by_name[category_name],
                    "attributes": {f: fields[f] for f in attribute_fields},
                }
            )
        return annotations

    def build(self) -> CocoDocument:
        self.validate_image_references()
        self.validate_bboxes()

        image_id_by_path = self.assign_image_ids()
        self.validate_annotation_ids()
        used_image_relative_paths = self.get_used_image_relative_paths()

        images = self.build_image_records(
            image_id_by_path,
            used_image_relative_paths,
        )

        categories, category_id_by_name = self.build_categories()

        annotations = self.build_annotations(image_id_by_path, category_id_by_name)
        return {
            "images": images,
            "annotations": annotations,
            "categories": categories,
        }

    def count_images_with_detections(self) -> int:
        """Number of images that have at least one item referencing them."""
        items_image_paths = {
            PurePosixPath(item.fields[self._options.image_name_column])
            for item in self._items
            if not item.skipped
        }
        return len(items_image_paths & self._image_relative_paths.keys())


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------


def print_summary(
    coco: CocoDocument,
    *,
    images_with_detections: int,
    output_path: Path,
    dropbox_link: str | None,
) -> None:
    print()
    print(f"{Fore.CYAN}Summary:")
    print(f"  Categories:  {len(coco['categories'])}")
    print(
        f"  Images:      {len(coco['images'])} "
        f"({images_with_detections} with detections)"
    )
    print(f"  Annotations: {len(coco['annotations'])}")
    print(f"  Output:      {output_path}")
    if dropbox_link:
        print(f"  Dropbox:     {dropbox_link}")


def main() -> None:
    args = parse_args()

    access_token = os.environ.get("DROPBOX_ACCESS_TOKEN")
    if not access_token:
        die("DROPBOX_ACCESS_TOKEN env var is not set.")

    with DropboxClient(access_token) as client:
        # Cheap checks first: download CSV and validate its fields before
        # paying for a recursive image listing.
        rows, headers = load_dropbox_csv_rows(
            client, args.metadata_csv_path_dropbox
        )
        ensure_required_fields(headers, args)

        image_index = list_dropbox_image_index(
            client, args.images_path_dropbox, args.base_folder
        )

        def resolve_image_url(relative_path: PurePosixPath) -> str:
            return client.get_or_create_shareable_url(
                PurePosixPath(image_index[relative_path]["path_lower"])
            )

        def probe_image_dimensions(relative_path: PurePosixPath) -> tuple[int, int]:
            img_bytes = client.download(
                PurePosixPath(image_index[relative_path]["path_lower"])
            )
            with Image.open(io.BytesIO(img_bytes)) as im:
                return im.size

        print(image_index.keys())

        builder = CocoBuilder(
            options=BuilderOptions.from_args(args),
            items=rows,
            fields=headers,
            image_relative_paths=image_index.keys(),
            resolve_image_url=resolve_image_url,
            probe_image_dimensions=(
                probe_image_dimensions if args.should_probe_dimensions else None
            ),
            image_source_label=str(args.base_folder),
        )
        coco = builder.build()

        write_output(coco, args.output_path)
        dropbox_link: str | None = None
        if args.should_upload_to_dropbox:
            dropbox_link = upload_coco_to_dropbox(
                client, coco, args.base_folder, args.output_path
            )

    print_summary(
        coco,
        images_with_detections=builder.count_images_with_detections(),
        output_path=args.output_path,
        dropbox_link=dropbox_link,
    )


if __name__ == "__main__":
    main()
