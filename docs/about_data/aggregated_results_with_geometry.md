---
title: Aggregated Results (with Geometry)
parent: About the Data
nav_order: 6
permalink: /docs/about_data/aggregated_results_with_geometry/
---

# Aggregated Results (with Geometry)
Same task-level aggregation as [Aggregated Results](aggregated_results.md), but delivered as a GeoJSON `FeatureCollection` — the task polygon lives on each feature's `geometry` instead of being a WKT column.

## Schema

One feature per task. Property names match [Aggregated Results](aggregated_results.md) minus `geom` (the geometry is on the feature itself). Each feature's `geometry` is a `MultiPolygon` (EPSG:4326).

## Sample download

A 10-row preview is shipped alongside these docs for reference. **It is not the live dataset** — for the full export, see the [MapSwipe data page](https://mapswipe.org/en/data/). The live file is delivered as gzipped GeoJSON (`.geojson.gz`) — unzip before use; the sample below is already decompressed.

- `agg_results_by_task_{project_id}_geom.geojson`, e.g. [agg_results_by_task_2962_geom.geojson](/assets/docs/about_data/files/project_exports/agg_results_by_task_2962_geom.geojson)
