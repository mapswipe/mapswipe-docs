---
title: Locate Objects
parent: Project Types
nav_order: 7
permalink: /project_types/locate_objects/
---

# Project Type - Locate Objects

Unlike Find Features, which asks whether an object is present anywhere in a full imagery tile, Locate Objects asks *where* within the tile it is. A single imagery tile is shown per screen, virtually subdivided into a grid of smaller mini tiles (2x2, 4x4, or 8x8, chosen by the project manager). Contributors tap the mini tile(s) that contain an object:

- One tap (highlighted green) — a single object is present in that mini tile.
- Two taps (highlighted yellow) — multiple objects are present in that mini tile.
- No tap — no object in that mini tile.

The mini-tile grid is a virtual subdivision of the same tile/zoom level (quad-tree style), not a request for higher-zoom imagery. The output is intended to produce AI-ready training datasets (e.g. for HOT's fAIr), so results capture per-mini-tile classification rather than a single yes/no per tile.

![](/assets/project_types/project_types/images/locate-objects.png)

Locate Objects projects have `projectType = 9`.

## Project
In addition to the common project fields documented in the [data model](../project_types.md), Locate Objects projects carry the following project-type-specific fields:

| Parameter             | Type            | Description                                                                                                                          |
|------------------------|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **zoomLevel**          | int             | Web Mercator zoom level at which tiles are served.                                                                                   |
| **tileServer**         | object          | Raster tile server configuration — includes a server `name`, `url`, `credits`, and an optional `apiKey`.                             |
| **subGridSize**        | enum (string)   | Size of the virtual mini-tile grid each screen's tile is subdivided into: `2x2` (4 partitions), `4x4` (16 partitions), or `8x8` (64 partitions). |
| **exportMetaKey**      | string          | Key of an additional metadata entry attached to exports (e.g. `"building"`).                                                         |
| **exportMetaValue**    | string          | Value of that additional metadata entry (e.g. `"roof_top"`).                                                                         |
| **customOptions**      | list (optional) | Custom answer options for classifying a mini tile (each with a value, title, description, icon, iconColor, and optional sub-options) — overrides the default No / Single Feature / Multiple Features choices. |

## Group
Locate Objects groups have no project-type-specific fields beyond the [common group fields](../project_types.md#groups), plus the tile-map-service bounding-box coordinates shared with Find Features:

| Parameter | Type | Description                                     |
|-----------|------|--------------------------------------------------|
| **xMax**  | int  | Maximum tile-X coordinate covered by the group.  |
| **xMin**  | int  | Minimum tile-X coordinate covered by the group.  |
| **yMax**  | int  | Maximum tile-Y coordinate covered by the group.  |
| **yMin**  | int  | Minimum tile-Y coordinate covered by the group.  |

## Task
Each task is a single imagery tile, identical in shape to a Find Features task; the mini-tile grid shown to the contributor is derived client-side from `subGridSize` rather than stored per-task.

| Parameter    | Type   | Description                                                                                                    |
|--------------|--------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **taskId**   | string | ID of the task, formatted as `{zoomLevel}-{tileX}-{tileY}`.                                                    |
| **tileX**    | int    | Tile-X coordinate of the task at `zoomLevel`.                                                                  |
| **tileY**    | int    | Tile-Y coordinate of the task at `zoomLevel`.                                                                  |
| **geometry** | string | Polygon geometry of the tile, generated from `tileX`, `tileY` and `zoomLevel`.                                  |
| **url**      | string | Tile URL for the imagery at `tileX`, `tileY`, `zoomLevel`.                                                      |

## Result
Locate Objects deviates from the [common result shape](../project_types.md#results): instead of a single int per task, each entry in `results` (keyed by `taskId`) is a **list of ints** — one value per mini-tile partition, ordered by partition index. A `subGridSize` of `2x2` yields a 4-value list, `4x4` a 16-value list, `8x8` a 64-value list.

```
results: {
  "9-267-352": [1, 0, 0, 2, ...]
}
```

Each value uses the same integer encoding as `customOptions` (or the fallback below when none are supplied). When exported, the backend explodes each list into one row per partition, adding a `task_partition_index` column set to the value's position in the list.

When the project creator does not supply `customOptions`, the backend falls back to the following defaults:

| Value | Title             | Description                                              |
|-------|-------------------|-----------------------------------------------------------|
| `0`   | No                | The mini tile does not contain a feature.                 |
| `1`   | Single Feature    | The mini tile contains a single feature.                  |
| `2`   | Multiple Features | The mini tile contains multiple features.                 |
