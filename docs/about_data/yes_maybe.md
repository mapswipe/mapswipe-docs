---
title: Moderate to High Agreement Yes Maybe Geometries
parent: About the Data
nav_order: 14
permalink: /docs/about_data/yes_maybe/
---

# Moderate to High Agreement Yes Maybe Geometries
This dataset contains all results where at least 35% of users submitted a "yes" or "maybe" classification. The output dataset depicts the union of all selected results.

## Schema

One feature per merged yes/maybe area, with the following `properties`:

| Name     | Type     | Description                                                                           |
| -------- | -------- | ------------------------------------------------------------------------------------- |
| id       | integer  | A sequential ID for the geometry. It has no connection to the MapSwipe data model.    |
| geometry | geometry | A polygon geometry representing the merged "yes" / "maybe" area of one or more tasks. |

## Sample download

A 10-row preview is shipped alongside these docs for reference. **It is not the live dataset** — for the full export, see the [MapSwipe data page](https://mapswipe.org/en/data/). The live file is delivered as GeoJSON (`.geojson`).

- `yes_maybe_{project_id}.geojson`, e.g. [yes_maybe_2962.geojson](/assets/docs/about_data/files/project_exports/yes_maybe_2962.geojson)
