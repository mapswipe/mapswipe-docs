---
title: Overview
nav_order: 2
permalink: /docs/overview/
---

# MapSwipe Overview

## A typical MapSwipe workflow

1. Project managers upload information about their projects (e.g. area of interest, objects to look for) to backend, which will sync information to Firebase in realtime database, using the **manager dashboard**.
2. A tutorial must be attached to the projects using existing tutorials or a new one in the final phase of project creation before the publishing it.
3. After the project is published from the **manager dashboard**, relevant groups and tasks are created in the backend and synced with Firebase
4. The users of the MapSwipe app contribute to the projects and submit their results via app which will be stored in backend as well as Firebase realtime database. The **firebase rules** ensure, that app users can only change pre-defined parts of the firebase realtime database.
5. Once new results are submitted, the **backend** and **firebase functions** generate real-time statistics and update the progress of groups, compute project level statistics and user statistics in the backend and firebase realtime database.
6. All results are synchronized with **backend** and **firebase** on defined basis (e.g. every 10 minutes). The backend database holds all MapSwipe results for long term storage. Once results are synced in the backend database, they will be deleted in Firebase realtime database by the workers.
7. Based on the data in the backend, the **backend** generates aggregated data and statistics (e.g. as CSV files). The data is served by the backend's GraphQL endpoint (the older nginx-served REST API is no longer used).

For the architectural picture behind this workflow — old vs. new architecture and the individual components — see [System Architecture](/docs/system_architecture/).
