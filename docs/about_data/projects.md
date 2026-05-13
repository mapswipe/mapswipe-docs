---
title: Projects Overview
parent: About the Data
nav_order: 1
permalink: /docs/about_data/projects/
---

# Projects Overview

A flat CSV catalog of every MapSwipe project — identifiers, status, area, contribution counts, and a geometry summary, one row per project.

## Schema

One row per project, with the following columns:

| Name                           | Type    | Description                                                                                                                                                                                            |
| ------------------------------ | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| id                             | integer | The numeric ID of the project in the revamped system, replacing the alphanumeric project_id from the old system.                                                                                       |
| firebase_id                    | string  | The alphanumeric ID of the project from the old Firebase system.                                                                                                                                       |
| name                           | string  | The name of the project as displayed in the app including project type, topic, region, number, and requesting organization. (e.g., "Find Buildings in Manbhawan - Manbhawan (1) Togglecorp").          |
| description                    | string  | The project description displayed in the app on the project page, detailing the purpose and tasks (e.g., scanning satellite imagery for buildings or earthquake damage).                               |
| look_for                       | string  | What users should look for in the project (e.g., buildings, houses, paved roads, potholes, cars).                                                                                                      |
| project_type                   | integer | The type of the project, represented as a numeric code (e.g., 1=Find features, 2=Validate footprints, 3=Compare dates, 4=Check completeness, 7=View streets, 10=Assess Images).                        |
| project_type_display           | string  | Human-readable name of the project type corresponding to the project_type code (e.g., "Find features", "Validate footprints", "Compare dates", "Check completeness", "View streets", "Assess Images"). |
| organization_name              | string  | The name of the organization requesting and responsible for the project (e.g., Togglecorp, HeiGIT).                                                                                                    |
| image_url                      | string  | URL to the project image displayed in the app.                                                                                                                                                         |
| created_at                     | string  | The date and time when the project was created, in ISO format with timezone (e.g., "2025-09-15 07:58:29.863248+00:00").                                                                                |
| status                         | integer | Numeric code representing the project status (e.g., 30=Processing Failed, 40=Processed, 70=Withdrawn, 75=Finished, 80=Discarded).                                                                      |
| status_display                 | string  | Human-readable status of the project, corresponding to the status code (e.g., "Processing Failed", "Processed", "Withdrawn", "Finished", "Discarded").                                                 |
| area_sqkm                      | float   | The size of the project area in square kilometers.                                                                                                                                                     |
| centroid                       | string  | The centroid of the project geometry as a WKT POINT (EPSG:4326), e.g. `POINT(3.6169 6.6249)`.                                                                                                          |
| geom                           | string  | The geometry of the project region as WKT geometry, prefixed with SRID=4326 and wrapped in GEOMETRYCOLLECTION (e.g., "SRID=4326;GEOMETRYCOLLECTION (POLYGON (...))").                                  |
| progress                       | float   | The mapping progress of the project as a fraction (0.0 = none, 1.0 = complete).                                                                                                                        |
| number_of_contributor_users    | integer | The number of distinct users who contributed to this project.                                                                                                                                          |
| number_of_results              | integer | The total number of results for all tasks.                                                                                                                                                             |
| number_of_results_for_progress | integer | The number of results considered for progress calculation, excluding redundant mappings.                                                                                                               |
| last_contribution_date         | string  | The date of the most recent contribution to the project (YYYY-MM-DD).                                                                                                                                  |

## Sample download

A 10-row preview is shipped alongside these docs for reference. **It is not the live dataset** — for the full export, see the [MapSwipe data page](https://mapswipe.org/en/data/).

- [projects.csv](/assets/docs/about_data/files/global_exports/projects.csv)

## Additions in New Architecture
The following fields have been added in the export after the architecture revamp
- **project_type_display**: Short name of the task type (e.g., "Find Features", "Validate Footprints").
- **status**: Numeric code for the project’s current state (10=Draft, 30=Processing Failed, 40=Processed, 70=Withdrawn, 75=Finished, 80=Discarded).
- **status_display**: Human-readable project state (Finished, Withdrawn, Discarded…).
