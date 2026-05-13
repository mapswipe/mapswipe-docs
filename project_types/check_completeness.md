---
title: Check Completeness
parent: Project Types
nav_order: 5
permalink: /project_types/check_completeness/
---

# Project Type - Check Completeness
Similar to the Find Features project, to create a Check Completeness project, you need to add all information and upload a bounding polygon as well as fill in some information about your project.

## Projects
Below you can find an example for a Check Completeness project in firebase. The structure and creation steps follow the similar pattern of the Find Features project type.

```json
{
  "contributorCount": 0,
  "created": "2025-09-25T13:48:39.455579+00:00",
  "createdBy": "5kYxvxiVgTRsi1DlgIdedLMcAJQ2",
  "groupMaxSize": 25,
  "groupSize": 25,
  "isFeatured": false,
  "language": "en-us",
  "lookFor": "buildings",
  "name": "Completeness buildings - Chandragiri, Nepal (1) Togglecorp",
  "overlayTileServer": {
    "type": "vector",
    "vector": {
      "circleColor": "#ffffff",
      "circleOpacity": 1,
      "circleRadius": 3,
      "fillColor": "#2196f3",
      "fillOpacity": 0.25,
      "lineColor": "#03a9f4",
      "lineDasharray": [
        3,
        2
      ],
      "lineOpacity": 1,
      "lineWidth": 2,
      "tileServer": {
        "credits": "Map data from OpenStreetMap",
        "maxZoom": 14,
        "minZoom": 0,
        "name": "openStreetMap",
        "sourceLayer": "buildings",
        "url": "https://vector.osm.org/shortbread_v1/{z}/{x}/{y}.mvt"
      }
    }
  },
  "progress": 0,
  "projectDetails": "n/a",
  "projectId": "01K60J464ZGTDXNHH7J50ZGM8V",
  "projectInstruction": "Look for buildings",
  "projectNumber": 1,
  "projectRegion": "Chandragiri, Nepal",
  "projectTopic": "buildings",
  "projectTopicKey": "completeness buildings - chandragiri, nepal (1) togglecorp",
  "projectType": 4,
  "requestingOrganisation": "Togglecorp",
  "requiredResults": 396,
  "resultCount": 0,
  "status": "active",
  "tileServer": {
    "apiKey": "AopsdXjtTu-IwNoCTiZBtgRJ1g7yPkzAi65nXplc-eLJwZHYlAIf2yuSY_Kjg3Wn",
    "credits": "© 2019 Microsoft Corporation, Earthstar Geographics SIO",
    "name": "bing",
    "url": "https://ecn.t0.tiles.virtualearth.net/tiles/a{quad_key}.jpeg?g=7505&mkt=en-US&token={apiKey}"
  },
  "tileServerB": {
    "apiKey": "",
    "credits": "n/a",
    "name": "custom",
    "url": "https://raw.githubusercontent.com/mapswipe/mapswipe-assets/refs/heads/main/images/raster-layer-404-message.png"
  },
  "tutorialId": "tutorial_01K5GZBZJJ62CVE4DRQJ6VAGNR",
  "verificationNumber": 3,
  "zoomLevel": 18
}
```

## Groups

| Parameter    | Description                                                                                          |
|--------------|------------------------------------------------------------------------------------------------------|
| **Geometry** | The Check Completeness groups save the bounding box coordinates in fields labeled xMax, xMin, yMax and yMin similar to the Find Features groups |

```json
{
  "finishedCount": 0,
  "groupId": "g101",
  "numberOfTasks": 48,
  "progress": 0,
  "projectId": "01K60J464ZGTDXNHH7J50ZGM8V",
  "requiredCount": 3,
  "xMax": "193104",
  "xMin": "193089",
  "yMax": "110101",
  "yMin": "110099"
}
```

## Tasks
Tasks are saved for tutorials, since their spatial information can be derived from the spatial extent of the corresponding group. Here, the tutorials are saved based on the project that it is derived from.

| Parameter                           | Description                                                                                                                                                                                                                                                                                                                                                                            |
|-------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| *Project Type Specific Information* |                                                                                                                                                                                                                                                                                                                                                                                        |
| **Tile X**                          | The x coordinate characterises the longitudinal position of the tile in the overall tile map system taken the zoom level into account. The x coordinates increase from west to east starting at a longitude of -180 degrees.                                                                                                                                                           |
| **Tile Y**                          | The y coordinate characterises the latitudinal position of the tile in the overall tile map system taken the zoom level into account. The latitude is clipped to range from circa -85 to 85 degrees. The y coordinates increase from north to south starting at a latitude of around 85 degrees.                                                                                       |
| **Geometry**                        | Each task has a polygon geometry, which can be generated by its x, y and z coordinates. At the equator the task geometry is a square with an edge length of around 150 metres covering circa 0.0225 square kilometres. Due to the web Mercator projector the task geometry will be clinched with increasing distance to the equator. At the same time the area per task will decrease. |
| **Tile URL**                        | The tile URL points to the specific tile image described by the x, y, and z coordinates. Usually, the image has a resolution of 256 x 256 pixels. However, some providers also generate image tiles with higher resolution (e.g. 512 x 512 pixels).                                                                                                                                    |

Below is an example json for a tutorial project, as can be seen on the three extra attributes screen, referenceAnswer and taskID_real.
```json
{
  "geometry": "",
  "groupId": 101,
  "projectId": "tutorial_01K5JJ14GTQF2HTM29F6BF1VZ7",
  "referenceAnswer": 1,
  "screen": 1,
  "taskId": "16-101-131073",
  "taskId_real": "16-48022-27374",
  "taskX": 101,
  "taskY": 131073,
  "url": "https://ecn.t0.tiles.virtualearth.net/tiles/a1231303132212330.jpeg?g=7505&mkt=en-US&token=AopsdXjtTu-IwNoCTiZBtgRJ1g7yPkzAi65nXplc-eLJwZHYlAIf2yuSY_Kjg3Wn",
  "urlB": "https://raw.githubusercontent.com/mapswipe/mapswipe-assets/refs/heads/main/images/raster-layer-404-message.png"
}
```

## Results
Results contain information on the user classifications. However, only "Yes" (1), "Maybe" (2) and "Bad Imagery" (3) classifications are stored as results.
Whenever users indicates "No" by just swiping to the next set of tasks, no data entry is created. "No" classifications can only be modelled retrospectively for groups where a user also submitted at least one "Yes", "Maybe" or "Bad Imagery" classification.
