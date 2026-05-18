---
title: Tasks
parent: About the Data
nav_order: 10
permalink: /docs/about_data/tasks/
---

# Tasks
This lists tasks, their identifiers, groups, and geometric polygons for a specific project.

## Schema

One row per task, with the following columns:

| Name                | Type    | Description                                                                                                 |
| ------------------- | ------- | ----------------------------------------------------------------------------------------------------------- |
| project_internal_id | integer | Internal numeric ID of the project.                                                                         |
| group_internal_id   | integer | Internal numeric ID of the group containing the task.                                                       |
| task_internal_id    | integer | Internal numeric ID of the task.                                                                            |
| project_id          | string  | The project identifier. Usually a ULID for new projects; legacy Firebase-style for older migrated projects. |
| group_id            | string  | Public group identifier within the project.                                                                 |
| task_id             | string  | Public task identifier; for tile-based projects formatted as `TileZ-TileX-TileY`.                           |
| geom                | string  | Task area as WKT MULTIPOLYGON (EPSG:4326).                                                                  |
| tile_z              | integer | Tile zoom level (tile-based project types only).                                                            |
| tile_x              | integer | Tile X index (tile-based project types only).                                                               |
| tile_y              | integer | Tile Y index (tile-based project types only).                                                               |
| url                 | string  | URL to the satellite imagery tile shown to users (tile-based project types only).                           |

## Sample download

A 10-row preview is shipped alongside these docs for reference. **It is not the live dataset** — for the full export, see the [MapSwipe data page](https://mapswipe.org/en/data/). The live file is delivered as gzipped CSV (`.csv.gz`) — unzip before use; the sample below is already decompressed.

- `tasks_{project_id}.csv`, e.g. [tasks_2962.csv](/assets/docs/about_data/files/project_exports/tasks_2962.csv)
