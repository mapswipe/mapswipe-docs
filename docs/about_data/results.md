---
title: Results
parent: About the Data
nav_order: 9
permalink: /docs/about_data/results/
---

# Results
This gives you the unfiltered MapSwipe results — individual task contributions, timings, and the classification each user submitted.

## Schema

One row per submission, with the following columns:

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

## Sample download

A 10-row preview is shipped alongside these docs for reference. **It is not the live dataset** — for the full export, see the [MapSwipe data page](https://mapswipe.org/en/data/). The live file is delivered as gzipped CSV (`.csv.gz`) — unzip before use; the sample below is already decompressed.

- `results_{project_id}.csv`, e.g. [results_2962.csv](/assets/docs/about_data/files/project_exports/results_2962.csv)
