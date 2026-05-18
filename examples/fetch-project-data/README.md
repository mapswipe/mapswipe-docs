---
title: Fetch Project Data
parent: Examples and Scripts
nav_order: 2
permalink: /examples/fetch-project-data/
---

# Fetch Project Data

A read-only script that downloads every per-project data export listed in the [About the Data](/docs/about_data/) page (aggregated results, tasks, groups, users, history, results, HOT Tasking Manager geometries, yes/maybe geometries) from the public MapSwipe GraphQL backend, decompresses gzipped payloads, and optionally samples the first N records of each file.

> [!NOTE]
> This script needs no credentials. It only reads from `publicProjects` on the public backend.

> [!CAUTION]
> Ongoing updates to MapSwipe may render this script **out-of-date**.

Utility script: [`run.py`](run.py)

## What it does

1. Hits `https://backend.mapswipe.org/health-check/` once to obtain a CSRF cookie.
2. Posts a `ProjectExports` query to `https://backend.mapswipe.org/graphql/` filtered server-side by `id` (the project's GraphQL ID).
3. Iterates over every `export*` field on the returned project, downloads the file at `file.url`, and gunzips it when the filename ends in `.gz` (or the payload starts with the gzip magic bytes).
4. With `--sample N`, keeps only the first N rows of each CSV (after the header) or the first N features of each GeoJSON `FeatureCollection`. Without `--sample`, files are written through verbatim.
5. Writes every file directly into the `--out` directory. The script does not append the project id — pass a project-specific path if you want one project per directory.

## Why `id` and not `firebaseId`

The backend schema's `ProjectFilter` exposes `id`, `oldId`, and a handful of non-string fields — but **not** `firebaseId`. `oldId` is empty for most projects in the new system, so `id` is the only viable filter. The result projection still includes `firebaseId` and `oldId` so you can sanity-check the match. See [`schema.graphql`](https://raw.githubusercontent.com/mapswipe/mapswipe-backend/refs/heads/develop/schema.graphql) for the full filter input.

## Requirements

- Python 3.10+ (uses `int | None`-style union syntax and `tuple[...]` generics)
- No third-party packages — `urllib` + `http.cookiejar` + `gzip` + `json` only

## Usage

```bash
uv run run.py <projectId>
```

By default this writes to `assets/docs/about_data/files/` relative to the repo root. The script does not auto-create a per-project subdirectory — pass `--out` with a project-specific path if you want isolation.

### Options

| Flag | Default | Meaning |
| ---- | ------- | ------- |
| `<projectId>` *(positional)* | required | The value of `ProjectType.id` (the project's GraphQL ID, used as the filter). |
| `--out PATH` | `assets/docs/about_data/files/` (relative to the repo root) | Output directory. Files are written directly here; no project subdirectory is appended. |
| `--sample N` | unset (full download) | Keep only the first N records per CSV / GeoJSON file. |

### Examples

Download the full set of exports for a project:

```bash
uv run run.py 2962 --out assets/docs/about_data/files/project_exports
```

Sample 10 rows / features per file (useful for generating illustrative samples for the docs):

```bash
uv run run.py 2962 --sample 10 --out assets/docs/about_data/files/project_exports
```

Write somewhere outside the repo:

```bash
uv run run.py 2962 --out /tmp/mapswipe-exports
```

## Output layout

The per-project files all include the project id in their name, so multiple projects can share the same `--out` directory. Given `--out assets/docs/about_data/files/project_exports` for project `2962`:

```
assets/docs/about_data/files/project_exports/
├── agg_results_by_task_2962.csv
├── agg_results_by_task_2962_geom.geojson
├── groups_2962.csv
├── history_2962.csv
├── hot_tm_2962.geojson
├── results_2962.csv
├── tasks_2962.csv
├── users_2962.csv
└── yes_maybe_2962.geojson
```

Filenames come from `file.name` returned by the API; only the basename is used (any path segments in the URL are stripped).

## Troubleshooting

> [!IMPORTANT]
> **`No project matching '<id>'`** — the `id` filter didn't return a project. The slug in `mapswipe.org/en/projects/<slug>/` is the *Firebase* style identifier, **not** the GraphQL `id`. You need to look up the project's `id` value (the integer / ULID returned by `publicProjects` on the result type). The script does not currently do that lookup for you.

> [!NOTE]
> **`CSRF cookie 'MAPSWIPE-PROD-CSRFTOKEN' not set by health-check`** — the cookie name baked into the script is the production one. If you point it at the staging or alpha instance, change `CSRFTOKEN_KEY` at the top of the script (e.g. `MAPSWIPE-STAGE-CSRFTOKEN`, `MAPSWIPE-ALPHA-2-CSRFTOKEN`).

## Generating GraphQL queries

Use the GraphiQL explorer to experiment with the schema:
<https://backend.mapswipe.org/graphql/>
