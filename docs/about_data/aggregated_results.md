---
title: Aggregated Results
parent: About the Data
nav_order: 5
permalink: /docs/about_data/aggregated_results/
---

# Aggregated Results
This gives you the unfiltered MapSwipe results aggregated on the task level. This is most suited if you want to apply some custom data processing with the MapSwipe data, e.g. select only specific tasks. If you want geometries on each task instead of a `geom` column, see [Aggregated Results (with Geometry)](/docs/about_data/aggregated_results_with_geometry/).

## Schema

One row per task, with the following columns:

| Name                | Type    | Description                                                                                                                                                                                     |
| ------------------- | ------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| idx                 | integer | Sequential row index.                                                                                                                                                                           |
| task_id             | string  | The ID of the task. For tile-based project types (e.g. Find Features) this is a composition of `TileZ-TileX-TileY`.                                                                             |
| 0_count             | integer | The number of users who marked this task as 0, e.g. "no building" for Find Features.                                                                                                            |
| 1_count             | integer | The number of users who marked this task as 1, e.g. "building" for Find Features.                                                                                                               |
| 2_count             | integer | The number of users who marked this task as 2, e.g. "maybe" for Find Features.                                                                                                                  |
| 3_count             | integer | The number of users who marked this task as 3, e.g. "bad imagery" for Find Features.                                                                                                            |
| total_count         | integer | The total number of users who mapped this task.                                                                                                                                                 |
| 0_share             | float   | `0_count` divided by `total_count`. This gives you the share of all users who marked as 0.                                                                                                      |
| 1_share             | float   | `1_count` divided by `total_count`. This gives you the share of all users who marked as 1.                                                                                                      |
| 2_share             | float   | `2_count` divided by `total_count`. This gives you the share of all users who marked as 2.                                                                                                      |
| 3_share             | float   | `3_count` divided by `total_count`. This gives you the share of all users who marked as 3.                                                                                                      |
| agreement           | float   | [Scott's Pi](https://en.wikipedia.org/wiki/Scott%27s_Pi) inter-rater reliability. 1.0 means all users agreed; lower values indicate disagreement. Empty when only one user has mapped the task. |
| quadkey             | string  | Bing Maps quadkey identifying the tile (tile-based project types only).                                                                                                                         |
| project_internal_id | integer | The internal numeric project ID.                                                                                                                                                                |
| group_internal_id   | integer | The internal numeric group ID for the group this task belongs to.                                                                                                                               |
| task_internal_id    | integer | The internal numeric task ID.                                                                                                                                                                   |
| geom                | string  | The geometry of this task as WKT (MULTIPOLYGON, EPSG:4326).                                                                                                                                     |
| tile_z              | integer | Tile zoom level (tile-based project types only).                                                                                                                                                |
| tile_x              | integer | Tile X index (tile-based project types only).                                                                                                                                                   |
| tile_y              | integer | Tile Y index (tile-based project types only).                                                                                                                                                   |
| url                 | string  | URL to the satellite imagery tile shown to users (tile-based project types only).                                                                                                               |

Additionally, project type specific data can be found here. E.g. Validate projects which were created based on OSM data, will have data describing the original OSM object included.

## Sample download

A 10-row preview is shipped alongside these docs for reference. **It is not the live dataset** — for the full export, see the [MapSwipe data page](https://mapswipe.org/en/data/). The live file is delivered as gzipped CSV (`.csv.gz`) — unzip before use; the sample below is already decompressed.

- `agg_results_by_task_{project_id}.csv`, e.g. [agg_results_by_task_2962.csv](/assets/docs/about_data/files/project_exports/agg_results_by_task_2962.csv)
