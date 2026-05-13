---
title: HOT Tasking Manager Geometries
parent: About the Data
nav_order: 13
permalink: /docs/about_data/hot_tm/
---

# HOT Tasking Manager Geometries
This dataset contains shapes that are ready to use in the HOT Tasking Manager. Currently, the geometries consist of maximum 15 MapSwipe Tasks, where at least 35% of all users indicated the presence of a building by classifying as "yes" or "maybe".

## Schema

One feature per merged geometry, with the following `properties`:

| Name     | Type     | Description                                                                                                                                                                |
| -------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| group_id | integer  | A ID for the geometry. It has no connection to the MapSwipe data model.                                                                                                    |
| geometry | geometry | A polygon geometry representing the selected MapSwipe tasks. In our GIS workflow we further aggregate and simplify the geometry, hence they kind of look like easter eggs. |

## Sample download

A 10-row preview is shipped alongside these docs for reference. **It is not the live dataset** — for the full export, see the [MapSwipe data page](https://mapswipe.org/en/data/). The live file is delivered as GeoJSON (`.geojson`).

- `hot_tm_{project_id}.geojson`, e.g. [hot_tm_2962.geojson](/assets/docs/about_data/files/project_exports/hot_tm_2962.geojson)
