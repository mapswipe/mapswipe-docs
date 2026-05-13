---
title: About the Data
nav_order: 3
permalink: /docs/about_data/
---

# About the Data
Swiping is just the beginning. MapSwipe data is created by our users and accessible to the entire community. Through the [MapSwipe website](https://mapswipe.org/en/data/) you can see where we've mapped, which organizations are requesting data, and how many individuals contribute to our impact. When using MapSwipe data, all you have to do is credit the MapSwipe contributors. Here you find a more detailed description of the data available.

## Global Exports
- **projects.csv**
- **projects_geom.geojson**
- **projects_centroid.geojson**
- **project_stats_by_types.csv**

> [!IMPORTANT]
> You can download the latest dataset from the website https://mapswipe.org/en/data/ (Search for `Download all projects`)

### Export: projects.csv
The export contains data of all the projects in MapSwipe.

#### File
- `projects.csv`, e.g. [projects.csv](/assets/docs/about_data/files/global_exports/projects.csv)

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

#### New Additions in New Architecture
The following fields have been added in the export after the architecture revamp
- **project_type_display**: Short name of the task type (e.g., "Find Features", "Validate Footprints").
- **status**: Numeric code for the project’s current state (10=Draft, 30=Processing Failed, 40=Processed, 70=Withdrawn, 75=Finished, 80=Discarded).
- **status_display**: Human-readable project state (Finished, Withdrawn, Discarded…).

### Export: projects_geom.geojson
A GeoJSON `FeatureCollection` with one `Feature` per MapSwipe project. Each feature carries the same metadata as `projects.csv` (minus `geom`, since the geometry is on the feature itself) and a `geometry` of type `GeometryCollection`.

#### File
- `projects_geom.geojson`, e.g. [projects_geom.geojson](/assets/docs/about_data/files/global_exports/projects_geom.geojson)

| Name                           | Type    | Description                                                                                                                                                                       |
| ------------------------------ | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| id                             | string  | The numeric project ID, serialized as a string in GeoJSON properties.                                                                                                             |
| firebase_id                    | string  | The alphanumeric ID of the project from the old Firebase system.                                                                                                                  |
| name                           | string  | The name of the project as displayed in the app.                                                                                                                                  |
| description                    | string  | The project description displayed in the app on the project page.                                                                                                                 |
| look_for                       | string  | What users should look for in the project (e.g., buildings, houses, paved roads).                                                                                                 |
| project_type                   | string  | The project type code (serialized as a string), e.g. `1`=Find features, `2`=Validate footprints, `3`=Compare dates, `4`=Check completeness, `7`=View streets, `10`=Assess Images. |
| project_type_display           | string  | Human-readable name of the project type.                                                                                                                                          |
| organization_name              | string  | The name of the organization requesting the project.                                                                                                                              |
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

#### New Additions in New Architecture
The following fields have been added in the export after the architecture revamp
- **project_type_display**: Short name of the task type (e.g., "Find Features", "Validate Footprints").
- **status_display**: Human-readable project state (Finished, Withdrawn, Discarded…).
- **number_of_contributor_users**: Total unique volunteers who tapped on this project.
- **number_of_results**: Every single swipe ever made in the project.
- **number_of_results_for_progress**: Swipes that actually moved the progress bar (excludes extras).
- **last_contribution_date**: Date of the most recent swipe (YYYY-MM-DD).
- **progress**: % of the area fully mapped (0.0 = 0%, 1.0 = 100%).

### Export: projects_centroid.geojson
Same `FeatureCollection` and property schema as [`projects_geom.geojson`](#export-projects_geomgeojson), but each feature's `geometry` is a single `Point` (the project centroid) instead of a `GeometryCollection` of polygons. Use this when you want a lightweight overview map without the full project boundaries.

#### File
- `projects_centroid.geojson`, e.g. [projects_centroid.geojson](/assets/docs/about_data/files/global_exports/projects_centroid.geojson)

### Export: project_stats_by_types.csv
The newly added export contains aggregated stats for all MapSwipe projects, grouped by the 6 project types, instantly revealing each type's project count, total area covered, every swipe submitted, and average volunteers per project.

#### File
- `project_stats_by_types.csv`, e.g. [project_stats_by_types.csv](/assets/docs/about_data/files/global_exports/project_stats_by_types.csv)

| Name                                | Type    | Description                                                                                                                                                                                        |
| ----------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| project_type                        | integer | The numeric code representing the type of projects aggregated in this row (e.g., 1=Find features, 2=Validate footprints, 3=Compare dates, 4=Check completeness, 7=View streets, 10=Assess Images). |
| project_type_display                | string  | The human-readable name of the project type corresponding to the project_type code, as displayed in the app (e.g., "Find", "Validate", "Compare", "Completeness", "Street", "Validate Image").     |
| projects_count                      | integer | The total number of projects of the specific project type included in this aggregated statistic.                                                                                                   |
| total_area_sqkm                     | float   | The cumulative size of the project areas in square kilometers for all projects of the specific project type (may be empty for some project types).                                                 |
| total_number_of_results             | integer | The total number of task results submitted across all projects of the specific project type.                                                                                                       |
| total_number_of_results_progress    | integer | The total number of results considered for progress calculation across all projects of the specific project type, excluding redundant mappings beyond the required threshold.                      |
| average_number_of_users_per_project | float   | The average number of distinct users who contributed to projects of the specific project type, calculated as the total number of contributor users divided by the number of projects.              |


## Project Specific Exports
For project specific exports, we have taken the example of the following project:

> *Find Features - Find Buildings - Mozambique Floods 2026 - Chibuto (1) HOT — `id` `2962`, `firebaseId` `01KMMX0C9MG396SCV8W8CZ8RY3`*

### Aggregated Results
This gives you the unfiltered MapSwipe results. This is most suited if you want to apply some custom data processing with the MapSwipe data, e.g. select only specific tasks for machine learning. If you want to use MapSwipe data in the Tasking Manager you might look for the data described below.

#### Files
- `agg_results_by_task_{project_id}.csv`, e.g. [agg_results_by_task_2962.csv](/assets/docs/about_data/files/project_exports/agg_results_by_task_2962.csv)
- `agg_results_by_task_{project_id}_geom.geojson`, e.g. [agg_results_by_task_2962_geom.geojson](/assets/docs/about_data/files/project_exports/agg_results_by_task_2962_geom.geojson) (feature geometry is a `MultiPolygon`)

| Name                | Type    | Description                                                                                                                                                                                                                                                   |
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
| geom                | string  | (CSV only) The geometry of this task as WKT (MULTIPOLYGON, EPSG:4326).                                                                                                                          |
| tile_z              | integer | Tile zoom level (tile-based project types only).                                                                                                                                                |
| tile_x              | integer | Tile X index (tile-based project types only).                                                                                                                                                   |
| tile_y              | integer | Tile Y index (tile-based project types only).                                                                                                                                                   |
| url                 | string  | URL to the satellite imagery tile shown to users (tile-based project types only).                                                                                                               |

Additionally, project type specific data can be found here. E.g. Validate projects which were created based on OSM data, will have data describing the original OSM object included.

### HOT Tasking Manager Geometries
This gives you filtered MapSwipe data ready to be imported to the HOT Tasking Manager.
Currently, the geometries in this dataset consist of maximum 15 MapSwipe Tasks, where at least 35% of all users indicated the presence of a building by classifying as "yes" or "maybe".

#### File
- `hot_tm_{project_id}.geojson`, e.g. [hot_tm_2962.geojson](/assets/docs/about_data/files/project_exports/hot_tm_2962.geojson)


| Name     | Type     | Description                                                                                                                                                                |
| -------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| group_id | integer  | A ID for the geometry. It has no connection to the MapSwipe data model.                                                                                                    |
| geometry | geometry | A polygon geometry representing the selected MapSwipe tasks. In our GIS workflow we further aggregate and simplify the geometry, hence they kind of look like easter eggs. |

### Users
This gives you data on the users which contributed to a project.

#### File
- `users_{project_id}.csv`, e.g. [users_2962.csv](/assets/docs/about_data/files/project_exports/users_2962.csv)

| Name                        | Type      | Description                                                                                                                                                                   |
| --------------------------- | --------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| idx                         | integer   | Sequential row index.                                                                                                                                                         |
| project_id                  | string    | The project identifier. Usually a ULID for projects created in the new system; older projects migrated from the previous system may keep their legacy Firebase-style id here. |
| user_id                     | string    | The Firebase user ID of the contributor.                                                                                                                                      |
| username                    | string    | The display name of the contributor.                                                                                                                                          |
| groups_completed            | integer   | Number of groups the user completed.                                                                                                                                          |
| total_contributions         | integer   | Number of individual tasks the user completed.                                                                                                                                |
| agreeing_contributions      | integer   | Tasks where the user's result matches the aggregated result (e.g. tile has buildings).                                                                                        |
| disagreeing_contributions   | integer   | Tasks where the user's result differs from the aggregated result.                                                                                                             |
| simple_agreement_score      | float     | Share of the user's tasks that match the aggregated result. E.g. 0.8 means the user agreed with the majority on 80% of tiles. Empty if not yet computable.                    |

### Groups
This provides data on groups, their tasks, and progress for a specific project.

#### File
- `groups_{project_id}.csv`, e.g. [groups_2962.csv](/assets/docs/about_data/files/project_exports/groups_2962.csv)

| Name                     | Type    | Description                                                                                                 |
| ------------------------ | ------- | ----------------------------------------------------------------------------------------------------------- |
| group_internal_id        | integer | Internal numeric ID of the group.                                                                           |
| project_internal_id      | integer | Internal numeric ID of the project.                                                                         |
| group_id                 | string  | Public group identifier within the project (e.g. `g155`).                                                   |
| project_id               | string  | The project identifier. Usually a ULID for new projects; legacy Firebase-style for older migrated projects. |
| number_of_tasks          | integer | Total number of tasks in the group.                                                                         |
| required_count           | integer | Number of contributions required per task for completion.                                                   |
| finished_count           | integer | Number of contributions submitted toward the group's tasks.                                                 |
| progress                 | float   | Group progress as a fraction (0.0 = none, 1.0 = complete).                                                  |
| total_area               | float   | Combined area covered by the group's tasks, in square kilometers.                                           |
| time_spent_max_allowed   | float   | Maximum allowed mapping time for the group, in seconds.                                                     |
| number_of_users_required | integer | Number of distinct users required to contribute to the group's tasks.                                       |
| x_max                    | integer | Maximum tile X index across the group's tasks (tile-based project types only).                              |
| x_min                    | integer | Minimum tile X index across the group's tasks (tile-based project types only).                              |
| y_max                    | integer | Maximum tile Y index across the group's tasks (tile-based project types only).                              |
| y_min                    | integer | Minimum tile Y index across the group's tasks (tile-based project types only).                              |


### History
This tracks daily results, progress, and user contributions for a specific project.

#### File
- `history_{project_id}.csv`, e.g. [history_2962.csv](/assets/docs/about_data/files/project_exports/history_2962.csv)

| Name                            | Type    | Description                                                                                                  |
| ------------------------------- | ------- | ------------------------------------------------------------------------------------------------------------ |
| day                             | string  | The day this row aggregates, in `YYYY-MM-DD` format.                                                         |
| number_of_results               | integer | Total swipes submitted on this day.                                                                          |
| number_of_results_progress      | integer | Swipes from this day that count toward progress (excludes redundant mappings beyond the required threshold). |
| cum_number_of_results           | integer | Running total of all swipes submitted up to and including this day.                                          |
| cum_number_of_results_progress  | integer | Running total of progress-counting swipes up to and including this day.                                      |
| progress                        | float   | Project progress gained on this day (delta), as a fraction.                                                  |
| cum_progress                    | float   | Cumulative project progress up to and including this day, as a fraction (0.0 = 0%, 1.0 = 100%).              |
| number_of_users                 | integer | Distinct users who contributed on this day.                                                                  |
| number_of_new_users             | integer | Users who contributed for the first time on this day.                                                        |
| cum_number_of_users             | integer | Cumulative distinct users who have contributed up to and including this day.                                 |
| project_id                      | string  | The project identifier. Usually a ULID for new projects; legacy Firebase-style for older migrated projects.  |


### Results
This details individual task contributions, timings, and results by users in groups for a specific project.

#### File
- `results_{project_id}.csv`, e.g. [results_2962.csv](/assets/docs/about_data/files/project_exports/results_2962.csv)

| Name                | Type    | Description                                                                                                    |
| ------------------- | ------- | -------------------------------------------------------------------------------------------------------------- |
| project_internal_id | integer | Internal numeric ID of the project.                                                                            |
| group_internal_id   | integer | Internal numeric ID of the group containing the task.                                                          |
| task_internal_id    | integer | Internal numeric ID of the task.                                                                               |
| user_internal_id    | integer | Internal numeric ID of the user.                                                                               |
| project_id          | string  | The project identifier. Usually a ULID for new projects; legacy Firebase-style for older migrated projects.    |
| group_id            | string  | Public group identifier within the project (e.g. `g183`).                                                      |
| task_id             | string  | Public task identifier; for tile-based projects formatted as `TileZ-TileX-TileY`.                              |
| user_id             | string  | The Firebase user ID of the contributor.                                                                       |
| timestamp           | string  | When the result was recorded (ISO 8601 with timezone).                                                         |
| start_time          | string  | When the user started the task (ISO 8601 with timezone).                                                       |
| end_time            | string  | When the user finished the task (ISO 8601 with timezone).                                                      |
| app_version         | string  | MapSwipe app version that produced the result (e.g. `0.3.2`).                                                  |
| client_type         | string  | Client used to submit (e.g. `web`, `mobile`).                                                                  |
| result              | integer | The classification submitted by the user (e.g. 0 = no, 1 = yes, 2 = maybe, 3 = bad imagery for Find Features). |
| username            | string  | The display name of the contributor.                                                                           |


### Tasks
This lists tasks, their identifiers, groups, and geometric polygons for a specific project.

#### File
- `tasks_{project_id}.csv`, e.g. [tasks_2962.csv](/assets/docs/about_data/files/project_exports/tasks_2962.csv)

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

### Moderate to High
This provides GeoJSON polygons representing areas marked as 'yes' or 'maybe' in the project.

#### File
- `yes_maybe_{project_id}.geojson`, e.g. [yes_maybe_2962.geojson](/assets/docs/about_data/files/project_exports/yes_maybe_2962.geojson)

| Name     | Type     | Description                                                                           |
| -------- | -------- | ------------------------------------------------------------------------------------- |
| id       | integer  | A sequential ID for the geometry. It has no connection to the MapSwipe data model.    |
| geometry | geometry | A polygon geometry representing the merged "yes" / "maybe" area of one or more tasks. |
