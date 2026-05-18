---
title: Groups
parent: About the Data
nav_order: 7
permalink: /docs/about_data/groups/
---

# Groups
This provides data on groups, their tasks, and progress for a specific project.

## Schema

One row per group, with the following columns:

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

## Sample download

A 10-row preview is shipped alongside these docs for reference. **It is not the live dataset** — for the full export, see the [MapSwipe data page](https://mapswipe.org/en/data/). The live file is delivered as gzipped CSV (`.csv.gz`) — unzip before use; the sample below is already decompressed.

- `groups_{project_id}.csv`, e.g. [groups_2962.csv](/assets/docs/about_data/files/project_exports/groups_2962.csv)
