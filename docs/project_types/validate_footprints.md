---
title: Validate Footprints
parent: Project Types
nav_order: 2
permalink: /project_types/validate_footprints/
---

# Project Type - Validate Footprints

## Project
Validate Footprints can be supplied with geometries in three separate ways.
1. by specifying a HOT Tasking Manager Project ID and an object [filter](https://docs.ohsome.org/ohsome-api/v1/filter.html)
2. by specifying an url to the data (e.g. an [ohsomeAPI](https://docs.ohsome.org/ohsome-api/v1/) call)
3. by uploading an aoi and an object [filter](https://docs.ohsome.org/ohsome-api/v1/filter.html)


```json
{
  "TMId": "11193",
  "contributorCount": 1,
  "created": "2021-12-10T18:05:26.090515Z",
  "createdBy": "X0zTSyvY0khDfRwc99aQfIjTEPK2",
  "filter": "building=* and geometry:polygon",
  "groupMaxSize": 0,
  "groupSize": 30,
  "image": "https://firebasestorage.googleapis.com/v0/b/dev-mapswipe.appspot.com/o/projectImages%2Fimage.jpeg?alt=media",
  "inputType": "TMId",
  "isFeatured": false,
  "lookFor": "Buildings",
  "name": "OSM Building Validation - Indonesia (1)\nAmerican Red Cross",
  "progress": 0,
  "projectDetails": "The Red Cross Climate Centre, Indonesian Red Cross (Palang Merah Indonesia/PMI), IFRC, British Red Cross and Australian Red Cross are implementing a programme where the data contributed will be used by the Red Cross to assist in forecasting future disaster impacts, by knowing in advance what is likely to be impacted and its exposure and vulnerability. The information will help implementation of early action activities to take place before a disaster strikes, contributing to reduce risk, prepare for effective response and ultimately to strengthen community resilience.",
  "projectId": "-Mq_IVluLteQRS75gWej",
  "projectNumber": "1",
  "projectRegion": "Indonesia",
  "projectTopic": "OSM Building Validation",
  "projectType": 2,
  "requestingOrganisation": "American Red Cross",
  "requiredResults": 286302,
  "resultCount": 0,
  "status": "private_active",
  "teamId": "-Mq_EQlzqmYytCspuFSq",
  "tileServer": {
    "apiKey": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "credits": "© 2019 Maxar",
    "name": "maxar_premium",
    "url": "https://services.digitalglobe.com/earthservice/tmsaccess/tms/1.0.0/DigitalGlobe%3AImageryTileService@EPSG%3A3857@jpg/{z}/{x}/{y}.jpg?connectId={key}"
  },
  "tutorialId": "tutorial_-MO3ky5z--RY8PC1lONa",
  "verificationNumber": 3
}
```
## Group
The validate groups follow the standard group structure.
```json
{
  "finishedCount": 0,
  "groupId": "g100",
  "numberOfTasks": 30,
  "progress": 0,
  "projectId": "-Mq_FxTdV2QJHsxQcvFk",
  "requiredCount": 3
}
```

## Task

| Parameter                           | Description                                                                            |
|-------------------------------------|----------------------------------------------------------------------------------------|
| *Project Type Specific Information* |                                                                                        |
| **GeoJSON**                         | Each task has a polygon geometry, which usually outlines a building or another object. |

```json
{
  "feature_id": 0,
  "geojson": {
    "coordinates": [ [ [ 5.15910196973, 13.48686869581 ], [ 5.15937974751, 13.48686869581 ], [ 5.15937974751, 13.48742425137 ], [ 5.15910196973, 13.48742425137 ], [ 5.15910196973, 13.48686869581 ] ] ],
    "type": "Polygon"
  },
  "id": "13564_100_0",
  "properties": "feature_geometries, e.g. attributes from osm"
}
```

## Result
The result for a Validate Footprints project are explicitly given via the "yes", "no" and "not sure" buttons.
