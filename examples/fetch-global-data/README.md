---
title: Fetch Global Data
parent: Examples and Scripts
nav_order: 3
permalink: /examples/fetch-global-data/
---

# Fetch Global Data

A read-only script that downloads the four MapSwipe-wide data exports listed under [Global Exports](/docs/about_data/#global-exports) — `projects.csv`, `projects_geom.geojson`, `projects_centroid.geojson`, and `projects_stats_by_type.csv` — from the public GraphQL backend, decompresses gzipped payloads, and optionally samples the first N records of each file.

> [!NOTE]
> This script needs no credentials. It only reads from `globalExportAssets` on the public backend.

> [!CAUTION]
> Ongoing updates to MapSwipe may render this script **out-of-date**.

Utility script: [`run.py`](run.py)

## What it does

1. Hits `https://backend.mapswipe.org/health-check/` once to obtain a CSRF cookie.
2. Posts a `GlobalExports` query to `https://backend.mapswipe.org/graphql/`. The query returns one `GlobalExportAssetType` per export — currently `PROJECTS_CSV`, `PROJECTS_GEOM_GEOJSON`, `PROJECTS_CENTROID_GEOJSON`, and `PROJECT_STATS_BY_TYPES`.
3. Downloads the file at each `file.url` and gunzips it when the filename ends in `.gz` (or the payload starts with the gzip magic bytes).
4. With `--sample N`, keeps only the first N rows of each CSV (after the header) or the first N features of each GeoJSON `FeatureCollection`. Without `--sample`, files are written through verbatim.
5. Writes everything under `assets/docs/about_data/files/global/`.

## Requirements

- Python 3.10+
- No third-party packages — `urllib` + `http.cookiejar` + `gzip` + `json` only

## Usage

```bash
uv run run.py
```

### Options

| Flag | Default | Meaning |
| ---- | ------- | ------- |
| `--out PATH` | `assets/docs/about_data/files/global/` (relative to the repo root) | Output directory. |
| `--sample N` | unset (full download) | Keep only the first N records per CSV / GeoJSON file. |

### Examples

Download every global export in full:

```bash
uv run run.py
```

Sample 10 rows / features per file (useful for generating illustrative samples for the docs):

```bash
uv run run.py --sample 10
```

Write somewhere outside the repo:

```bash
uv run run.py --out /tmp/mapswipe-globals
```

## Output layout

```
assets/docs/about_data/files/global/
├── projects.csv
├── projects_geom.geojson
├── projects_centroid.geojson
└── project_stats_by_types.csv
```

Filenames come from `file.name` returned by the API; only the basename is used (any path segments in the URL are stripped).

## Troubleshooting

> [!NOTE]
> **`CSRF cookie 'MAPSWIPE-PROD-CSRFTOKEN' not set by health-check`** — the cookie name baked into the script is the production one. If you point it at the staging or alpha instance, change `CSRFTOKEN_KEY` at the top of the script (e.g. `MAPSWIPE-STAGE-CSRFTOKEN`, `MAPSWIPE-ALPHA-2-CSRFTOKEN`).

## Generating GraphQL queries

Use the GraphiQL explorer to experiment with the schema:
<https://backend.mapswipe.org/graphql/>
