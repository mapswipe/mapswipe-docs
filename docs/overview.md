---
title: Overview
nav_order: 2
permalink: /docs/overview/
---

# MapSwipe Overview

This page walks through the typical MapSwipe workflow, from a project manager setting up a project through to volunteers contributing results and the data being exported. For how the underlying components fit together, see [System Architecture](/docs/system_architecture/).

## A typical MapSwipe workflow

1. Project managers use the **Manager Dashboard** to upload project information (e.g. area of interest, objects to look for) to the backend, which syncs it to the Firebase Realtime Database.
2. In the final phase of project creation, a tutorial must be attached before the project can be published — either an existing shared tutorial or one specialised for the project.
3. Once the project is published from the **Manager Dashboard**, the backend creates the relevant groups and tasks and syncs them to Firebase.
4. Users of the MapSwipe app contribute to projects and submit their results through the app; these are stored in both the Firebase Realtime Database. **Firebase rules** ensure that app users can only change pre-defined parts of the Firebase Realtime Database.
5. As new results arrive, **Firebase functions** and the **backend** generate real-time statistics — updating group progress and computing project and user statistics.
6. Results are synchronised between the **backend** and **Firebase** on a defined schedule (e.g. every 10 minutes). The backend database holds all MapSwipe results for long-term storage; once results are synced and then deletes them from the Firebase Realtime Database.
7. The **backend** then generates aggregated data and statistics from this stored data and serves them via its GraphQL endpoint.
