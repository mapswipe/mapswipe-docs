---
title: History
parent: About the Data
nav_order: 8
permalink: /docs/about_data/history/
---

# History
This tracks daily results, progress, and user contributions for a specific project.

## Schema

One row per day, with the following columns:

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

## Sample download

A 10-row preview is shipped alongside these docs for reference. **It is not the live dataset** — for the full export, see the [MapSwipe data page](https://mapswipe.org/en/data/). The live file is delivered as CSV (`.csv`).

- `history_{project_id}.csv`, e.g. [history_2962.csv](/assets/docs/about_data/files/project_exports/history_2962.csv)
