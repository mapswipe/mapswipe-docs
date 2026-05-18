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

- [Projects Overview](/docs/about_data/projects/) (`projects.csv`) — every project in MapSwipe, one row per project.
- [Projects with Geometry](/docs/about_data/projects_geom/) (`projects_geom.geojson`) — project metadata + each project's area-of-interest polygon(s).
- [Projects with Centroid](/docs/about_data/projects_centroid/) (`projects_centroid.geojson`) — same metadata but with a single centroid point per project.
- [Project Type's Stats](/docs/about_data/project_stats_by_types/) (`project_stats_by_types.csv`) — aggregated stats grouped by project type.

## Project Specific Exports
Exports scoped to a single project. For the examples on the following pages we use:

> *Find Features - Find Buildings - Mozambique Floods 2026 - Chibuto (1) HOT — `id` `2962`, `firebaseId` `01KMMX0C9MG396SCV8W8CZ8RY3`*

- [Aggregated Results](/docs/about_data/aggregated_results/) — unfiltered MapSwipe results aggregated on the task level (CSV).
- [Aggregated Results (with Geometry)](/docs/about_data/aggregated_results_with_geometry/) — same data as Aggregated Results, delivered as a GeoJSON `FeatureCollection`.
- [Groups](/docs/about_data/groups/) — task groups and their progress.
- [History](/docs/about_data/history/) — daily activity timeline.
- [Results](/docs/about_data/results/) — individual user contributions per task.
- [Tasks](/docs/about_data/tasks/) — task identifiers and geometries.
- [Users](/docs/about_data/users/) — contributor stats for this project.
- [Area of Interest](/docs/about_data/area_of_interest/) — the project's region as GeoJSON.
- [HOT Tasking Manager Geometries](/docs/about_data/hot_tm/) — filtered geometries ready for import into HOT Tasking Manager.
- [Moderate to High Agreement Yes Maybe Geometries](/docs/about_data/yes_maybe/) — merged polygons of areas marked yes / maybe.
