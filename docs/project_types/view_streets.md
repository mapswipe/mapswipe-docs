---
title: View Streets
parent: Project Types
nav_order: 6
permalink: /project_types/view_streets/
---

# Project Type - View Streets

## Project
The View Streets project type takes an AOI geometry as an input and returns corresponding Mapillary images to MapSwipe.

```json
{
  "contributorCount": 1,
  "created": "2025-10-12T09:33:48.575137+00:00",
  "createdBy": "Tyf9vhtd8aZCgLlaRWQGzBE52w82",
  "customOptions": [
    {
      "description": "the shape does outline a building in the image",
      "icon": "checkmark-outline",
      "iconColor": "#388E3C",
      "title": "Yes",
      "value": 1
    },
    {
      "description": "the shape doesn't match a building in the image",
      "icon": "close-outline",
      "iconColor": "#D32F2F",
      "title": "No",
      "value": 0
    },
    {
      "description": "if you're not sure or unsure about the image",
      "icon": "remove-outline",
      "iconColor": "#616161",
      "title": "Not Sure",
      "value": 2
    }
  ],
  "groupMaxSize": 25,
  "groupSize": 25,
  "isFeatured": false,
  "language": "en-us",
  "lookFor": "Roads",
  "name": "View Streets - Street Mapping for Urban Planning in Inda - India (1) American Red Cross",
  "numberOfGroups": 7,
  "progress": 4,
  "projectDetails": "This project focuses on mapping streets and road networks in urban areas of India. Volunteers identify streets visible in satellite imagery to ensure they are included in the maps. The results will improve street-level map coverage for planning, navigation, and local services.",
  "projectId": "01K7BW9RMYQ6FCD98QFBAEN31K",
  "projectInstruction": "Look for",
  "projectNumber": 1,
  "projectRegion": "India",
  "projectTopic": "Street Mapping for Urban Planning in Inda",
  "projectTopicKey": "view streets - street mapping for urban planning in inda - india (1) american red cross",
  "projectType": 7,
  "requestingOrganisation": "American Red Cross",
  "requiredResults": 513,
  "resultCount": 0,
  "status": "active",
  "tutorialId": "tutorial_01K718A8H8XNY0EY66BCWZXG10",
  "verificationNumber": 3
}
```

## Group
The groups follow the standard Validate Footprints group structure.
```json
{
  "finishedCount" : 0,
  "groupId" : "g0",
  "numberOfTasks" : 25,
  "progress" : 0,
  "projectId" : "01K7BW9RMYQ6FCD98QFBAEN31K",
  "requiredCount" : 3
}
```

## Task
The task is a Base64-encoded, GZIP-compressed string. It can be decoded and decompressed to view the original content.

```json
{
  "g0": "H4sIAAAAAAAC/62Vu0pGQQyEX+Xn1BZJJlc7fy8goqCNiFiIiqCF4qUS390cbK0kbLnLR5idmVx/La9vL08Pdx/H98vuZiE+ie1lXZxenfvR/kHl+dF27/AMfLLsbJaP2/fn33daQcFKmgJNXy8f314+X39vH2n53tn8E81uJrAUdhRoFK1CocLGVmpik2x1A8CmAXLL0bEjNFn7OHHUrCKg9DAm93CeREtlpSiMXMQxiQazJxeReaFk9Buj2aXSisuwsY0FTEUeBaVRYxshDKvazCmjgoAUqZYsJaic1VrSIErO4T6cdIBKE0GmOSt285SEvCqy8zg6Nrcz1JoPM/hoQbEJa1vbUxGus1EPRCti3g7sqppkV3tDqdiim3W2oaLFCKCrxKh/cjSQghVdbe9uv5wVW6Wbdd2PPfms/Yiq49LsYsrC7NhYg95x5xaEh9dBry+zbJegi+oP9s0PuctVnukIAAA="
}
```

## Result
The results for a View Streets project, similar to the Validate Footprints project, are explicitly given via custom options that can be set by the project creator.
