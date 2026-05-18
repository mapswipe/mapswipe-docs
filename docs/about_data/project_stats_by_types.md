---
title: Project Type's Stats
parent: About the Data
nav_order: 4
permalink: /docs/about_data/project_stats_by_types/
---

# Project Type's Stats
The newly added export contains aggregated stats for all MapSwipe projects, grouped by the 6 project types, instantly revealing each type's project count, total area covered, every swipe submitted, and average volunteers per project.

## Schema

One row per project type, with the following columns:

| Name                                | Type    | Description                                                                                                                                                                                        |
| ----------------------------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| project_type                        | integer | The numeric code representing the type of projects aggregated in this row (e.g., 1=Find features, 2=Validate footprints, 3=Compare dates, 4=Check completeness, 7=View streets, 10=Assess Images). |
| project_type_display                | string  | The human-readable name of the project type corresponding to the project_type code, as displayed in the app (e.g., "Find", "Validate", "Compare", "Completeness", "Street", "Validate Image").     |
| projects_count                      | integer | The total number of projects of the specific project type included in this aggregated statistic.                                                                                                   |
| total_area_sqkm                     | float   | The cumulative size of the project areas in square kilometers for all projects of the specific project type (may be empty for some project types).                                                 |
| total_number_of_results             | integer | The total number of task results submitted across all projects of the specific project type.                                                                                                       |
| total_number_of_results_progress    | integer | The total number of results considered for progress calculation across all projects of the specific project type, excluding redundant mappings beyond the required threshold.                      |
| average_number_of_users_per_project | float   | The average number of distinct users who contributed to projects of the specific project type, calculated as the total number of contributor users divided by the number of projects.              |

## Sample download

A 10-row preview is shipped alongside these docs for reference. **It is not the live dataset** — for the full export, see the [MapSwipe data page](https://mapswipe.org/en/data/).

- [project_stats_by_types.csv](/assets/docs/about_data/files/global_exports/project_stats_by_types.csv)
