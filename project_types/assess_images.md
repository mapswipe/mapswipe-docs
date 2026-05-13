---
title: Assess Images
parent: Project Types
nav_order: 4
permalink: /project_types/assess_images/
---

# Project Type - Assess Images
## COCO File Format
The Assess Images project type is created using the following sample COCO json file, as shown in the [sample dataset](/assets/project_sample_data/assess_images/coco_sample.json).

## Project
Assess Images projects can be supplied with a COCO file

```
    {
      "contributorCount": 0,
      "created": "2025-10-17T09:33:25.446892+00:00",
      "createdBy": "23",
      "customOptions": [
        {
          "description": "the image contains the feature",
          "icon": "checkmark-outline",
          "iconColor": "#388E3C",
          "title": "Yes",
          "value": 1
        },
        {
          "description": "the image does not contain the feature",
          "icon": "close-outline",
          "iconColor": "#D32F2F",
          "title": "No",
          "value": 0
        },
        {
          "description": "it's not clear if the image contains the feature",
          "icon": "remove-outline",
          "iconColor": "#616161",
          "title": "Not Sure",
          "value": 2
        }
      ],
      "groupMaxSize": 10,
      "groupSize": 10,
      "isFeatured": false,
      "language": "en-us",
      "lookFor": "humans",
      "name": "Assess Images - Humans - Worldwide (1) Togglecorp (test)",
      "progress": 0,
      "projectDetails": "Look for humans",
      "projectId": "01K7RR8N268FRMXPN0P3186PSK",
      "projectInstruction": "Can you see any humans?",
      "projectNumber": 1,
      "projectRegion": "Worldwide",
      "projectTopic": "Humans",
      "projectTopicKey": "assess images - humans - worldwide (1) togglecorp (test)",
      "projectType": 10,
      "requestingOrganisation": "Togglecorp (test)",
      "requiredResults": 81,
      "resultCount": 0,
      "status": "active",
      "tutorialId": "tutorial_01K60ZMFGT7WRFH38W8PZ93V4M",
      "verificationNumber": 3
    }
```

## Group
The group tasks created in Firebase

```
    {
      "-OX8K9Ia2oSUkBSvJPrR": {
        "g100": {
          "groupId": "g100",
          "projectId": "01K7RR8N268FRMXPN0P3186PSK",
          "numberOfTasks": 25,
          "requiredCount": 3,
          "finishedCount": 0,
          "progress": 0
        },
        "g101": {
          "groupId": "g101",
          "projectId": "01K7RR8N268FRMXPN0P3186PSK",
          "numberOfTasks": 25,
          "requiredCount": 3,
          "finishedCount": 0,
          "progress": 0
        },
        "g102": {
          "groupId": "g102",
          "projectId": "01K7RR8N268FRMXPN0P3186PSK",
          "numberOfTasks": 25,
          "requiredCount": 3,
          "finishedCount": 0,
          "progress": 0
        },
        "g103": {
          "groupId": "g103",
          "projectId": "01K7RR8N268FRMXPN0P3186PSK",
          "numberOfTasks": 25,
          "requiredCount": 3,
          "finishedCount": 0,
          "progress": 0
        },
    }
```

## Task
The task structure of the Assess Images project type varies from the rest.
> Note: only task `g100` is added below

```
    [
      {
        "annotationId": "200887",
        "bbox": [
          388.66,
          69.92,
          109.41,
          277.62
        ],
        "fileName": "000000397133.jpg",
        "height": 427,
        "projectId": "01K7RR8N268FRMXPN0P3186PSK",
        "taskId": "200887",
        "url": "https://www.dropbox.com/scl/fi/qix2itz2ioncwct8iq65d/000000397133.jpg?rlkey=yqkvbfzmzxklp68d0zulj2ci4&st=vmg9ijfs&dl=1",
        "width": 640
      },
      {
        "annotationId": "1218137",
        "bbox": [
          0,
          262.81,
          62.16,
          36.77
        ],
        "fileName": "000000397133.jpg",
        "height": 427,
        "projectId": "01K7RR8N268FRMXPN0P3186PSK",
        "taskId": "1218137",
        "url": "https://www.dropbox.com/scl/fi/qix2itz2ioncwct8iq65d/000000397133.jpg?rlkey=yqkvbfzmzxklp68d0zulj2ci4&st=vmg9ijfs&dl=1",
        "width": 640
      },
      {
        "annotationId": "235634",
        "bbox": [
          47.19,
          296.12,
          28.3,
          33.17
        ],
        "fileName": "000000480985.jpg",
        "height": 500,
        "projectId": "01K7RR8N268FRMXPN0P3186PSK",
        "taskId": "235634",
        "url": "https://www.dropbox.com/scl/fi/vjdvvla0tyhfpde7yige9/000000480985.jpg?rlkey=35zs7wgdxpck58v5mz64jqt7u&st=2q3o8e37&dl=1",
        "width": 375
      },
      {
        "annotationId": "236267",
        "bbox": [
          32.75,
          298.94,
          16.52,
          29.22
        ],
        "fileName": "000000480985.jpg",
        "height": 500,
        "projectId": "01K7RR8N268FRMXPN0P3186PSK",
        "taskId": "236267",
        "url": "https://www.dropbox.com/scl/fi/vjdvvla0tyhfpde7yige9/000000480985.jpg?rlkey=35zs7wgdxpck58v5mz64jqt7u&st=2q3o8e37&dl=1",
        "width": 375
      },
      {
        "annotationId": "236973",
        "bbox": [
          320.16,
          275.05,
          27.06,
          104.53
        ],
        "fileName": "000000480985.jpg",
        "height": 500,
        "projectId": "01K7RR8N268FRMXPN0P3186PSK",
        "taskId": "236973",
        "url": "https://www.dropbox.com/scl/fi/vjdvvla0tyhfpde7yige9/000000480985.jpg?rlkey=35zs7wgdxpck58v5mz64jqt7u&st=2q3o8e37&dl=1",
        "width": 375
      },
      {
        "annotationId": "237362",
        "bbox": [
          10.05,
          302.96,
          13.7,
          25.69
        ],
        "fileName": "000000480985.jpg",
        "height": 500,
        "projectId": "01K7RR8N268FRMXPN0P3186PSK",
        "taskId": "237362",
        "url": "https://www.dropbox.com/scl/fi/vjdvvla0tyhfpde7yige9/000000480985.jpg?rlkey=35zs7wgdxpck58v5mz64jqt7u&st=2q3o8e37&dl=1",
        "width": 375
      },
      {
        "annotationId": "240624",
        "bbox": [
          266.37,
          293.13,
          23.97,
          88.96
        ],
        "fileName": "000000480985.jpg",
        "height": 500,
        "projectId": "01K7RR8N268FRMXPN0P3186PSK",
        "taskId": "240624",
        "url": "https://www.dropbox.com/scl/fi/vjdvvla0tyhfpde7yige9/000000480985.jpg?rlkey=35zs7wgdxpck58v5mz64jqt7u&st=2q3o8e37&dl=1",
        "width": 375
      },
      {
        "annotationId": "1729065",
        "bbox": [
          369.5,
          278.52,
          5.5,
          45.65
        ],
        "fileName": "000000480985.jpg",
        "height": 500,
        "projectId": "01K7RR8N268FRMXPN0P3186PSK",
        "taskId": "1729065",
        "url": "https://www.dropbox.com/scl/fi/vjdvvla0tyhfpde7yige9/000000480985.jpg?rlkey=35zs7wgdxpck58v5mz64jqt7u&st=2q3o8e37&dl=1",
        "width": 375
      },
      {
        "annotationId": "2155199",
        "bbox": [
          290.03,
          299.79,
          15.24,
          19.87
        ],
        "fileName": "000000480985.jpg",
        "height": 500,
        "projectId": "01K7RR8N268FRMXPN0P3186PSK",
        "taskId": "2155199",
        "url": "https://www.dropbox.com/scl/fi/vjdvvla0tyhfpde7yige9/000000480985.jpg?rlkey=35zs7wgdxpck58v5mz64jqt7u&st=2q3o8e37&dl=1",
        "width": 375
      },
      {
        "annotationId": "2161724",
        "bbox": [
          302.2,
          298.22,
          12.73,
          18.73
        ],
        "fileName": "000000480985.jpg",
        "height": 500,
        "projectId": "01K7RR8N268FRMXPN0P3186PSK",
        "taskId": "2161724",
        "url": "https://www.dropbox.com/scl/fi/vjdvvla0tyhfpde7yige9/000000480985.jpg?rlkey=35zs7wgdxpck58v5mz64jqt7u&st=2q3o8e37&dl=1",
        "width": 375
      }
    ]
```

## Result Structure
The result for Assess Images projects are explicitly given via the “yes”, “no” buttons (which are configurable custom options).
