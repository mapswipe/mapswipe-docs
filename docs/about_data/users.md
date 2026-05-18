---
title: Users
parent: About the Data
nav_order: 11
permalink: /docs/about_data/users/
---

# Users
This dataset contains information on the individual contributions per user. This tells you for instance the most active users of this project.

## Schema

One row per contributor, with the following columns:

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

## Sample download

A 10-row preview is shipped alongside these docs for reference. **It is not the live dataset** — for the full export, see the [MapSwipe data page](https://mapswipe.org/en/data/). The live file is delivered as gzipped CSV (`.csv.gz`) — unzip before use; the sample below is already decompressed.

- `users_{project_id}.csv`, e.g. [users_2962.csv](/assets/docs/about_data/files/project_exports/users_2962.csv)
