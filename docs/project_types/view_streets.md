---
title: View Streets
parent: Project Types
nav_order: 6
permalink: /project_types/view_streets/
---

# Project Type - View Streets

An imagery version of the Validate Footprint project type where users can look for a specific feature (set by the project managers) in a set of Mapillary images.

![](/assets/project_types/project_types/images/k9nzk7129lqaqztgp6d67mzad.png)

View Streets projects have `projectType = 7`.

## Project
The View Streets project type takes an AOI geometry as an input and returns corresponding Mapillary images to MapSwipe.

In addition to the common project fields documented in the [data model](/project_types/), View Streets projects carry the following project-type-specific fields:

| Parameter          | Type            | Description                                                                                                                        |
|--------------------|-----------------|------------------------------------------------------------------------------------------------------------------------------------|
| **customOptions**  | list (optional) | Custom answer options shown to the contributor (each with a value, title, description, icon, iconColor, and optional sub-options). |
| **numberOfGroups** | int             | Total number of groups generated for the project.                                                                                  |

## Group
View Streets groups have no project-type-specific fields beyond the [common group fields](/project_types/#groups). Each group is identified by:

| Parameter   | Type   | Description       |
|-------------|--------|-------------------|
| **groupId** | string | ID of the group.  |

## Task
The task payload is a Base64-encoded, GZIP-compressed string; clients decode and decompress it before rendering. Note that for View Streets the underlying `taskId` is an `int` rather than a `string`.

| Parameter   | Type   | Description                                |
|-------------|--------|--------------------------------------------|
| **taskId**  | int    | ID of the task (integer for View Streets). |
| **groupId** | string | ID of the group the task belongs to.       |

## Result
Results follow the [common result shape](/project_types/#results), with `results: dict[str, int]` keyed by `taskId`. The integer values come from each custom option's `value` defined on the project, since answers are given via custom options set by the project creator.

When the project creator does not supply `customOptions`, the backend falls back to the following defaults:

| Value | Title    | Description                                                  |
|-------|----------|--------------------------------------------------------------|
| `0`   | No       | The object you are looking for is NOT in the image.          |
| `1`   | Yes      | The object you are looking for is in the image.              |
| `2`   | Not Sure | You're not sure or there is bad imagery.                     |
