---
title: Projects with Geometry
parent: About the Data
nav_order: 2
permalink: /docs/about_data/projects_geom/
---

# Projects with Geometry
A GeoJSON `FeatureCollection` with one `Feature` per MapSwipe project. Each feature carries the same metadata as `projects.csv` (minus `geom`, since the geometry is on the feature itself) and a `geometry` of type `GeometryCollection`.

## Schema

One feature per project, with the following `properties`:

| Name                           | Type    | Description                                                                                                                                                                       |
| ------------------------------ | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| id                             | string  | The numeric project ID, serialized as a string in GeoJSON properties.                                                                                                             |
| firebase_id                    | string  | The alphanumeric ID of the project from the old Firebase system.                                                                                                                  |
| name                           | string  | The name of the project as displayed in the app.                                                                                                                                  |
| description                    | string  | The project description displayed in the app on the project page.                                                                                                                 |
| look_for                       | string  | What users should look for in the project (e.g., buildings, houses, paved roads).                                                                                                 |
| project_type                   | string  | The project type code (serialized as a string), e.g. `1`=Find features, `2`=Validate footprints, `3`=Compare dates, `4`=Check completeness, `7`=View streets, `10`=Assess Images. |
| project_type_display           | string  | Human-readable name of the project type.                                                                                                                                          |
| organization_name              | string  | The name of the organisation requesting the project.                                                                                                                              |
| image_url                      | string  | URL to the project image displayed in the app.                                                                                                                                    |
| created_at                     | string  | When the project was created, ISO timestamp with timezone.                                                                                                                        |
| status                         | string  | Project status code (serialized as a string), e.g. `30`=Processing Failed, `40`=Processed, `70`=Withdrawn, `75`=Finished, `80`=Discarded.                                         |
| status_display                 | string  | Human-readable project status.                                                                                                                                                    |
| area_sqkm                      | string  | Project area in square kilometers, serialized as a string.                                                                                                                        |
| centroid                       | string  | Centroid of the project geometry as WKT POINT (EPSG:4326).                                                                                                                        |
| progress                       | string  | Project progress as a fraction (0.0 – 1.0), serialized as a string.                                                                                                               |
| number_of_contributor_users    | string  | Distinct users who contributed to this project, serialized as a string.                                                                                                           |
| number_of_results              | string  | Total swipes submitted across all of the project's tasks, serialized as a string.                                                                                                 |
| number_of_results_for_progress | string  | Swipes that count toward progress (excludes redundant mappings beyond the required threshold), serialized as a string.                                                            |
| last_contribution_date         | string  | Date of the most recent contribution to the project (YYYY-MM-DD).                                                                                                                 |

The feature's `geometry` is a `GeometryCollection` containing the project's area-of-interest polygon(s) in EPSG:4326.

## Sample download

A 10-row preview is shipped alongside these docs for reference. **It is not the live dataset** — for the full export, see the [MapSwipe data page](https://mapswipe.org/en/data/).

- [projects_geom.geojson](/assets/docs/about_data/files/global_exports/projects_geom.geojson)

## Additions in New Architecture
The following fields have been added in the export after the architecture revamp
- **project_type_display**: Short name of the task type (e.g., "Find Features", "Validate Footprints").
- **status_display**: Human-readable project state (Finished, Withdrawn, Discarded…).
- **number_of_contributor_users**: Total unique volunteers who tapped on this project.
- **number_of_results**: Every single swipe ever made in the project.
- **number_of_results_for_progress**: Swipes that actually moved the progress bar (excludes extras).
- **last_contribution_date**: Date of the most recent swipe (YYYY-MM-DD).
- **progress**: % of the area fully mapped (0.0 = 0%, 1.0 = 100%).
