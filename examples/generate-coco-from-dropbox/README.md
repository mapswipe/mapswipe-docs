---
title: Generate COCO File from Dropbox
parent: Examples and Scripts
nav_order: 5
permalink: /examples/generate-coco-from-dropbox/
---

# Generate a COCO File from Dropbox

## Background

[Assess Images](../../docs/project_types/assess_images.md) projects are created from a COCO-format JSON file describing the images to be mapped. This page provides two Python scripts that generate such a file from a Dropbox folder, exposing image URLs as public Dropbox share links.

- **v1** — `generate_coco_from_dropbox.py`: builds a minimal COCO file (`{ "images": [...] }`) from a **flat folder of images**. No annotations, no categories. Useful when you only need to register images for mapping.
- **v2** — `generate_coco_with_annotations_from_dropbox.py`: builds a full COCO file (`images`, `annotations`, `categories`) from an **images folder paired with a CSV metadata file** that describes bounding-box annotations per image. Useful when you already have annotations and want to seed an Assess Images project with them.

> [!CAUTION]
> Ongoing updates to MapSwipe and Dropbox may render these scripts **out-of-date**.

> For the Google Drive equivalent see [Generate COCO File from Google Drive](../generate-coco-from-drive/README.md).

## Common Prerequisites

These apply to both scripts.

- A Dropbox account: <https://www.dropbox.com/register>.
- A new Dropbox app: <https://www.dropbox.com/developers/apps>.
  - **Choose an API:** Scoped access.
  - **Choose the type of access:** Full Dropbox.
  - **Name your app:** `your-app-name`.
- The following **Scoped App** permissions enabled on the app:
  - `files.metadata.read`
  - `files.content.write`
  - `files.content.read`
  - `sharing.write`
  - `sharing.read`
- A generated access token (from the app settings → **Generated access token**).
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed.

## v1 — From a Flat Image Directory

Utility script: [`generate_coco_from_dropbox.py`](generate_coco_from_dropbox.py)

Produces a minimal COCO file containing only an `images` array. Each image is given a public Dropbox share link as its `coco_url`. The resulting JSON is uploaded back into the same Dropbox folder.

### Additional Prerequisites

- A Dropbox folder containing the images to be exported (`.jpg`, `.jpeg`, `.png`, or `.webp`). The folder is listed **non-recursively** — only files in the top level are picked up.

### Creation Steps

1. Copy the folder path in Dropbox.
2. Copy the generated access token from Dropbox.
3. Run the script:

   ```bash
   # Help
   uv run generate_coco_from_dropbox.py --help

   # Usage
   uv run generate_coco_from_dropbox.py "DROPBOX_ACCESS_TOKEN" "FOLDER_PATHNAME_IN_DROPBOX" "DESTINATION_EXPORT_FILE_NAME_IN_DROPBOX"

   # Example
   uv run generate_coco_from_dropbox.py sl.yourAccessTokenHere "/COCO TEST" "coco_export.json"
   ```
4. Download the exported COCO JSON from the link printed in the terminal, or directly from your Dropbox folder.

## v2 — From an Images Directory with a Metadata CSV

Utility script: [`generate_coco_with_annotations_from_dropbox.py`](generate_coco_with_annotations_from_dropbox.py)

Produces a full COCO file (`images`, `annotations`, `categories`) by combining an images sub-folder with a CSV metadata file that describes one bounding-box annotation per row. Image URLs are resolved to public Dropbox share links. The output is written locally; uploading back to Dropbox is opt-in.

### Additional Prerequisites

- A Dropbox folder containing:
  - An images sub-folder (default: `images/`) with `.jpg`, `.jpeg`, `.png`, or `.webp` files. The folder is listed **recursively**.
  - A CSV metadata file (default: `metadata.csv`) with at least these columns:
    - `image_name` — image path relative to the images folder.
    - `boxes` — JSON-encoded 4-element list (e.g. `[x1, y1, x2, y2]`).
    - `type` — category name for the annotation.

    Additional columns are preserved as per-annotation `attributes`. All column names are configurable via flags.

### Creation Steps

1. Copy the folder path in Dropbox (the one containing the images sub-folder and the CSV).
2. Copy the generated access token from Dropbox and export it:

   ```bash
   export DROPBOX_ACCESS_TOKEN="sl.yourAccessTokenHere"
   ```
3. Run the script:

   ```bash
   # Help
   uv run generate_coco_with_annotations_from_dropbox.py --help

   # Usage
   uv run generate_coco_with_annotations_from_dropbox.py "FOLDER_PATHNAME_IN_DROPBOX" [options]

   # Example
   uv run generate_coco_with_annotations_from_dropbox.py "/Indonesia"

   # Example with custom columns, lenient mode, image-dimension probing, and upload
   uv run generate_coco_with_annotations_from_dropbox.py "/Indonesia" \
     --output ./indonesia.coco.json \
     --images-path images/ \
     --metadata-csv-path metadata.csv \
     --category-column type \
     --image-name-column image_name \
     --boxes-column boxes \
     --box-format xyxy \
     --lenient \
     --probe-dimensions \
     --upload-to-dropbox
   ```
4. Download the exported COCO JSON from the local path printed in the terminal (default: `./<base-folder-basename>.coco.json`). If `--upload-to-dropbox` was used, a temporary Dropbox link is also printed.

### Options

| Flag | Default | Purpose |
| --- | --- | --- |
| `--output` | `./<base-folder-basename>.coco.json` | Local path to write the COCO JSON. |
| `--images-path` | `images/` | Images folder, relative to the base folder (absolute Dropbox paths also accepted). |
| `--metadata-csv-path` | `metadata.csv` | CSV file path, relative to the base folder (absolute also accepted). |
| `--category-column` | `type` | CSV column used to derive COCO categories. |
| `--image-name-column` | `image_name` | CSV column with the image path relative to `--images-path`. |
| `--boxes-column` | `boxes` | CSV column with the bounding box (JSON-encoded 4-element list). |
| `--box-format` | `xyxy` | Format of the values in `--boxes-column`. `xyxy` is converted to COCO `xywh` on output. |
| `--annotation-id-column` | _(unset)_ | CSV column to use as annotation id (must be unique). Defaults to sequential 1..N. |
| `--image-id-column` | _(unset)_ | CSV column to use as image id (must be consistent per image). Defaults to sequential 1..N. |
| `--strict` / `--lenient` | `--strict` | Hard-error vs. skip-and-warn on rows referencing missing images or invalid boxes. |
| `--probe-dimensions` | `false` | Download each image and probe `width`/`height` with Pillow. |
| `--upload-to-dropbox` | `false` | Also upload the COCO JSON to `<base_folder>/<output basename>` in Dropbox. |
