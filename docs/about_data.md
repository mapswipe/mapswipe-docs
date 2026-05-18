---
title: About the Data
nav_order: 5
has_children: true
has_toc: false
permalink: /docs/about_data/
---

# About the Data
Swiping is just the beginning. MapSwipe data is created by our users and accessible to the entire community. Through the [MapSwipe website](https://mapswipe.org/en/data/) you can see where we've mapped, which organisations are requesting data, and how many individuals contribute to our impact. When using MapSwipe data, all you have to do is credit the MapSwipe contributors. Here you find a more detailed description of the data available.

> [!IMPORTANT]
> You can download the latest dataset from the website https://mapswipe.org/en/data/ (Search for `Download all projects`).

## Global Exports
Exports that describe the whole MapSwipe project catalog.

- [Projects Overview](about_data/projects.md) (`projects.csv`) — every project in MapSwipe, one row per project.
- [Projects with Geometry](about_data/projects_geom.md) (`projects_geom.geojson`) — project metadata + each project's area-of-interest polygon(s).
- [Projects with Centroid](about_data/projects_centroid.md) (`projects_centroid.geojson`) — same metadata but with a single centroid point per project.
- [Project Type's Stats](about_data/project_stats_by_types.md) (`project_stats_by_types.csv`) — aggregated stats grouped by project type.

## Project Specific Exports
Exports scoped to a single project. For the examples on the following pages we use:

> *Find Features - Find Buildings - Mozambique Floods 2026 - Chibuto (1) HOT — `id` `2962`, `firebaseId` `01KMMX0C9MG396SCV8W8CZ8RY3`*

- [Aggregated Results](about_data/aggregated_results.md) — unfiltered MapSwipe results aggregated on the task level (CSV).
- [Aggregated Results (with Geometry)](about_data/aggregated_results_with_geometry.md) — same data as Aggregated Results, delivered as a GeoJSON `FeatureCollection`.
- [Groups](about_data/groups.md) — task groups and their progress.
- [History](about_data/history.md) — daily activity timeline.
- [Results](about_data/results.md) — individual user contributions per task.
- [Tasks](about_data/tasks.md) — task identifiers and geometries.
- [Users](about_data/users.md) — contributor stats for this project.
- [Area of Interest](about_data/area_of_interest.md) — the project's region as GeoJSON.
- [HOT Tasking Manager Geometries](about_data/hot_tm.md) — filtered geometries ready for import into HOT Tasking Manager.
- [Moderate to High Agreement Yes Maybe Geometries](about_data/yes_maybe.md) — merged polygons of areas marked yes / maybe.
