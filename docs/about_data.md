# About the Data
Swiping is just the beginning. MapSwipe data is created by our users and accessible to the entire community. Through the [MapSwipe website](https://mapswipe.org/en/data/) you can see where we've mapped, which organizations are requesting data, and how many individuals contribute to our impact. When using MapSwipe data, all you have to do is credit the MapSwipe contributors. Here you find a more detailed description of the data available.

## Global Exports
- **projects.csv**
- **projects_geom.geojson**
- **projects_centroid.geojson**
- **project_types_data.csv**

> [!IMPORTANT]
> You can download the latest dataset from the website https://mapswipe.org/en/data/ (Search for `Download all projects`)

### Export: projects.csv
The export contains data of all the projects in MapSwipe.
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
| centroid                       | string  | The centroid of the project geometry as WKT geometry (often empty in the provided data).                                                                                                               |
| geom                           | string  | The geometry of the project region as WKT geometry, prefixed with SRID=4326 and wrapped in GEOMETRYCOLLECTION (e.g., "SRID=4326;GEOMETRYCOLLECTION (POLYGON (...))").                                  |
| progress                       | float   | The mapping progress of the project indicating incomplete or unstarted projects.                                                                                                                       |
| number_of_contributor_users    | integer | The number of distinct users who contributed to this project.                                                                                                                                          |
| number_of_results              | integer | The total number of results for all tasks.                                                                                                                                                             |
| number_of_results_for_progress | integer | The number of results considered for progress calculation, excluding redundant mappings.                                                                                                               |
| last_contribution_date         | string  | The date of the last contribution to the project (empty in the provided data).                                                                                                                         |

#### New Additions in New Architecture
The following fields have been added in the export after the architecture revamp
- **project_type_display**: Short name of the task type (e.g., "Find Features", "Validate Footprints").
- **status**: Numeric code for the project’s current state (10=Draft, 30=Processing Failed, 40=Processed, 70=Withdrawn, 75=Finished, 80=Discarded).
- **status_display**: Human-readable project state (Finished, Withdrawn, Discarded…).

### Export: projects_geom.geojson
This export contains MapSwipe projects with the following information.

- Name: Project title with type, location, and organization.
- Look For: The feature volunteers should identify (e.g., buildings, roads, people).
- Type: Project category: Find Features, Assess Images, Compare Dates, View Streets.
- Status: Active, Finished, Withdrawn, or Processed.
- Area: Project size in km² (if available).
- Image: Sample image illustrating the task.

| Name                          | Type          | Look For    | Status    | Area (km²) |
| ----------------------------- | ------------- | ----------- | --------- | ---------- |
| Find Buildings in Manbhawan   | Find Features | Buildings   | Withdrawn | 0.004      |
| Validate Image - Mustang      | Assess IMages | Person      | Processed | –          |
| View Streets - Antsirabe      | View Streets  | Paved Roads | Withdrawn | 3.37       |
| Find Affected Areas - Pokhara | Find Features | House       | Finished  | 6.49       |
| Compare - Earthquake Impact   | Compare Dates | House       | Processed | 11.08      |

#### New Additions in New Architecture
The following fields have been added in the export after the architecture revamp
- **project_type_display**: Short name of the task type (e.g., "Find Features", "Validate Footprints").
- **status_display**: Human-readable project state (Finished, Withdrawn, Discarded…).
- **number_of_contributors**: Total unique volunteers who tapped on this project.
- **number_of_results**: Every single swipe ever made in the project.
- **number_of_results_for_progress**: Swipes that actually moved the progress bar (excludes extras).
- **last_contribution_date**: Date of the most recent swipe (YYYY-MM-DD).
- **progress**: % of the area fully mapped (0.0 = 0%, 1.0 = 100%).

### Export: projects_centroid.geojson
This export is similar to the export with projects_geom.geojson

### Export: projects_stats_by_type.csv
The newly added export contains aggregated stats for all MapSwipe projects, grouped by the 6 project types, instantly revealing each type’s project count, total area covered, every swipe submitted, and average volunteers per project.

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

> *Find Features - Public Health - Maluku, Democratic Republic of Congo (1) American Red Cross (-M56eeMCZ5VeOHjJN4Bx)*

### Aggregated Results
This gives you the unfiltered MapSwipe results. This is most suited if you want to apply some custom data processing with the MapSwipe data, e.g. select only specific tasks for machine learning. If you want to use MapSwipe data in the Tasking Manager you might look for the data described below.

#### Files
- `aggregated_results_{project_id}.csv`, e.g. [agg\_results\_-M56eeMCZ5VeOHjJN4Bx.csv](/assets/docs/about_data/files/agg_results_-M56eeMCZ5VeOHjJN4Bx.csv.gz)
- `aggregated_results_{project_id}.geojson`, e.g. [agg\_results\_-M56eeMCZ5VeOHjJN4Bx.geojson](/assets/docs/about_data/files/agg_results_-M56eeMCZ5VeOHjJN4Bx_geom.geojson.gz)

| Name        | Type     | Description                                                                                                                                                                                                                                                    |
|-------------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| idx         |  integer | -                                                                                                                                                                                                                                                              |
| task_id     | string   | The ID of the task, for BuildArea projects this is a composition of `TileZ-TileX-TileY`                                                                                                                                                                        |
| 0_count     | integer  | The number of users who marked this task as 0, e.g. "no building" for BuildArea Project Type.                                                                                                                                                                  |
| 1_count     | integer  | The number of users who marked this task as 1, e.g. "building" for BuildArea Project Type.                                                                                                                                                                     |
| 2_count     | integer  | The number of users who marked this task as 2, e.g. "maybe" for BuildArea Project Type.                                                                                                                                                                        |
| 3_count     | integer  | The number of users who marked this task as 3, e.g. "bad imagery" for BuildArea Project Type.                                                                                                                                                                  |
| total_count | integer  | The total number of users who mapped this task.                                                                                                                                                                                                                |
| 0_share     | float    | 0_count divived by total_count. This gives you the share of all users who marked as 0.                                                                                                                                                                         |
| 1_share     | float    | 1_count divived by total_count. This gives you the share of all users who marked as 1.                                                                                                                                                                         |
| 2_share     | float    | 2_count divived by total_count. This gives you the share of all users who marked as 2.                                                                                                                                                                         |
| 3_share     | float    | 3_count divived by total_count. This gives you the share of all users who marked as 3.                                                                                                                                                                         |
| agreement   | float    | This is defined as [Scott's Pi](https://en.wikipedia.org/wiki/Scott%27s_Pi) and gives you an understanding of inter-rater reliability. The value is 1.0 if all users agree, e.g. all users classify as "building". If users disagree this value will be lower. |
| geom        | string   | The geometry of this task as WKT geometry.                                                                                                                                                                                                                     |

Additionally, project type specific data can be found here. E.g. Validate projects which were created based on OSM data, will have data describing the original OSM object included.

### HOT Tasking Manager Geometries
This gives you filtered MapSwipe data ready to be imported to the HOT Tasking Manager.
Currently, the geometries in this dataset consist of maximum 15 MapSwipe Tasks, where at least 35% of all users indicated the presence of a building by classifying as "yes" or "maybe".

#### File
- `hot_tm_{project_id}.geojson`, e.g. [hot\_tm\_-M56eeMCZ5VeOHjJN4Bx.geojson](/assets/docs/about_data/files/hot_tm_-M56eeMCZ5VeOHjJN4Bx.geojson)


| Name     | Type     | Description                                                                                                                                                                |
| -------- | -------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| group_id | integer  | A ID for the geometry. It has no connection to the MapSwipe data model.                                                                                                    |
| geometry | geometry | A polygon geometry representing the selected MapSwipe tasks. In our GIS workflow we further aggregate and simplify the geometry, hence they kind of look like easter eggs. |

### Users
This gives you data on the users which contributed to a project.

#### File
- `users_{project_id}.csv`, e.g. [users.csv](/assets/docs/about_data/files/users_-M56eeMCZ5VeOHjJN4Bx.csv.gz)

| Name                      | Type    | Description                                                                                                                                                      |
|---------------------------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| idx                       | integer | -                                                                                                                                                                |
| groups_completed          | integer | Number of groups completed                                                                                                                                       |
| total_contributions       | integer | Number of tasks completed                                                                                                                                        |
| agreeing_contributions    | integer | Tasks with the same result as the final result (e.g. Tile has buildings).                                                                                        |
| disagreeing_contributions | integer | Tasks with other result as the final result.                                                                                                                     |
| simple_agreement_score    | float   | Share of tasks which had the same result as the final result. E.g. 0.8 would mean that the user labeled 80% of the tiles the same way as the majority of voters. |

### Groups
This provides data on groups, their tasks, and progress for a specific project.

#### File
- `groups_{project_id}.csv`, e.g. [groups.csv](/assets/docs/about_data/files/groups_-M56eeMCZ5VeOHjJN4Bx.csv.gz)

| Name                     | Type    | Description                                                               |
| ------------------------ | ------- | ------------------------------------------------------------------------- |
| project_id               | string  | Unique identifier for the project to which the group belongs.             |
| group_id                 | string  | Unique identifier for the group within the project.                       |
| number_of_tasks          | integer | Total number of tasks assigned to the group.                              |
| finished_count           | integer | Number of tasks in the group that have been completed.                    |
| required_count           | integer | Number of contributions required per task for completion.                 |
| progress                 | float   | Progress of the group’s tasks, likely as a fraction (e.g., 0.0 for none). |
| project_type_specifics   | string  | JSON string containing additional details like groupId, coordinates, etc. |
| number_of_users_required | integer | Number of users required to contribute to the group’s tasks.              |


### History
This tracks daily results, progress, and user contributions for a specific project.

#### File
- `history_{project_id}.csv`, e.g. [history.csv](/assets/docs/about_data/files/history_-M56eeMCZ5VeOHjJN4Bx.csv)

| Name                     | Type    | Description                                                               |
| ------------------------ | ------- | ------------------------------------------------------------------------- |
| project_id               | string  | Unique identifier for the project to which the group belongs.             |
| group_id                 | string  | Unique identifier for the group within the project.                       |
| number_of_tasks          | integer | Total number of tasks assigned to the group.                              |
| finished_count           | integer | Number of tasks in the group that have been completed.                    |
| required_count           | integer | Number of contributions required per task for completion.                 |
| progress                 | float   | Progress of the group’s tasks, likely as a fraction (e.g., 0.0 for none). |
| project_type_specifics   | string  | JSON string containing additional details like groupId, coordinates, etc. |
| number_of_users_required | integer | Number of users required to contribute to the group’s tasks.              |


### Results
This details individual task contributions, timings, and results by users in groups for a specific project.

#### File
- `results_{project_id}.csv`, e.g. [results.csv](/assets/docs/about_data/files/results_-M56eeMCZ5VeOHjJN4Bx.csv.gz)

| Name       | Type    | Description                                                                  |
| ---------- | ------- | ---------------------------------------------------------------------------- |
| project_id | string  | Unique identifier for the project to which the result belongs.               |
| group_id   | string  | Identifier for the group containing the task.                                |
| user_id    | string  | Unique identifier for the user who completed the task.                       |
| task_id    | string  | Identifier for the specific task, often in format like zoom-x-y coordinates. |
| timestamp  | string  | Timestamp when the result was recorded (in YYYY-MM-DD HH:MM:SS format).      |
| start_time | string  | Start time of the task (in YYYY-MM-DD HH:MM:SS format).                      |
| end_time   | string  | End time of the task (in YYYY-MM-DD HH:MM:SS format).                        |
| result     | integer | The outcome or classification result of the task (e.g., 0 for negative).     |


### Tasks
This lists tasks, their identifiers, groups, and geometric polygons for a specific project.

#### File
- `tasks_{project_id}.csv`, e.g. [tasks.csv](/assets/docs/about_data/files/tasks_-M56eeMCZ5VeOHjJN4Bx.csv.gz)

| Name       | Type   | Description                                                                                                           |
| ---------- | ------ | --------------------------------------------------------------------------------------------------------------------- |
| project_id | string | Unique identifier for the project to which the task belongs.                                                          |
| group_id   | string | Identifier for the group containing the task.                                                                         |
| task_id    | string | Unique identifier for the task, often in format like zoom-x-y coordinates.                                            |
| geom       | string | Geometric boundary of the task area in WKT (Well-Known Text) MULTIPOLYGON format with longitude-latitude coordinates. |

### Moderate to High
This provides GeoJSON polygons representing areas marked as 'yes' or 'maybe' in the project.

#### File
- `yes_maybe_{project_id}.geojson`, e.g. [yes_maybe.geojson](/assets/docs/about_data/files/yes_maybe_-M56eeMCZ5VeOHjJN4Bx.geojson)
