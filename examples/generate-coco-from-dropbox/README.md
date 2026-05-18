---
title: Generate COCO File from Dropbox
parent: Examples and Scripts
nav_order: 5
permalink: /examples/generate-coco-from-dropbox/
---

# Generate a COCO File from Dropbox

## Background

[Assess Images](/project_types/assess_images/) projects are created from a COCO-format JSON file describing the images to be mapped. This page provides a Python script that produces a minimal COCO file (`{ "images": [...] }`) from a folder of images hosted on Dropbox, so they can be referenced by public URL. The script also uploads the resulting JSON back to the same Dropbox folder.

> [!CAUTION]
> Ongoing updates to MapSwipe and Dropbox may render this script **out-of-date**.

Utility script: [`generate_coco_from_dropbox.py`](generate_coco_from_dropbox.py)

> For the Google Drive equivalent see [Generate COCO File from Google Drive](/examples/generate-coco-from-drive/).

## Prerequisites

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
- A Dropbox folder containing the images to be exported.

## Creation Steps

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
