---
title: Generate COCO File from Google Drive
parent: Examples and Scripts
nav_order: 4
permalink: /examples/generate-coco-from-drive/
---

# Generate a COCO File from Google Drive

## Background

[Assess Images](/project_types/assess_images/) projects are created from a COCO-format JSON file describing the images to be mapped. This page provides a Google Apps Script that produces a minimal COCO file (`{ "images": [...] }`) from a folder of images hosted on Google Drive, so they can be referenced by public URL.

> [!CAUTION]
> Ongoing updates to MapSwipe and Google Drive may render this script **out-of-date**.

Utility script: [`generate_coco_from_drive.js`](generate_coco_from_drive.js)

> For the Dropbox equivalent see [Generate COCO File from Dropbox](/examples/generate-coco-from-dropbox/).

## Prerequisites

- A Google account.
- Your image files stored in a **public** Google Drive folder.
- Access to Google Apps Script at <https://script.google.com>.

## Creation Steps

1. **Create a Google Apps Script project.**
   - Go to <https://script.google.com>.
   - Click on **New Project**.
   - Rename the project to `your-project-name`.
2. **Paste the utility script.**
   - Replace the default code with the contents of [`generate_coco_from_drive.js`](generate_coco_from_drive.js).
3. **Replace placeholder values.**
   - Replace `your_coco_export.json` with your desired output filename.
   - Replace `your_public_folder_id` with the ID of your Google Drive folder.

   > The folder ID is the alphanumeric string that appears after `/folders/` in the URL.
   > Example: `drive.google.com/drive/folders/`**`1prcCevijN5mubTllB2kr5ki1gjh_IO4u`**`?usp=sharing`
4. **Run the script.**
   - Save the project using the floppy-disk 💾 icon.
   - Press **Run**.
   - Accept the authorization prompts the first time you run the script.
5. **View the COCO JSON output.**
   - Go to **View → Logs**.
   - Copy the Google Drive URL where the COCO file was generated.
   - Download the JSON file.
