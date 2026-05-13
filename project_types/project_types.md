---
title: Project Types
nav_order: 5
has_children: true
permalink: /project_types/
---

# MapSwipe Project Types and Data Model
## MapSwipe's Crowdsourcing Approach
The MapSwipe crowdsourcing workflow is designed following an approach already presented by [Albuquerque et al. (2016)](https://www.mdpi.com/2072-4292/8/10/859). The main ideas about MapSwipe's crowdsourcing approach (and many other crowdsourcing tasks) lies in
1. **Defining** the mapping challenge by posing a simple question (e.g. "Which areas are inhabited in South Kivu?")
2. **Dividing** the overall challenge into many smaller manageable components (e.g. *groups* and *tasks* based on satellite imagery tiles)
3. **Distributing** *groups* and *tasks* to many users redundantly (e.g. every area gets mapped by at least three different users)
4. **Aggregating** all responses (*results*) per *task* from different users  to reach a final solution (e.g. by choosing the majority vote)

The MapSwipe backend now supports 6 **project types**. Each project type formulates a specific kind of mapping challenge.

| Name                                                | ID  | Description                                                                                                                                                                                                                                                                                                                                                                                                  | Screenshot                                                            |
| --------------------------------------------------- | --- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------- |
| [Find Features](/project_types/find_features.md)        | 1   | A 6 squares layout is used for this project type. By tapping you can classify a tile of satellite imagery as *yes*, *maybe* or *bad_imagery*. Project managers can define which objects to look for, e.g. "buildings". Furthermore, they can specify the tile server of the background satellite imagery, e.g. "bing" or a custom tile server.                                                               | ![](/assets/project_types/project_types/images/qyioxvg73f3vdmmu6wlvrx3ib.png)        |
| [Validate Footprints](/project_types/validate_footprints.md)  | 2   | An image with a footprint overlay. The question is whether this footprint is correctly approximating a structure on the shown image, which can be answered with *yes*, *no* or *Not sure*. Additionally, a button is shown which hides the footprint overlay.                                                                                                                                                | ![](/assets/project_types/project_types/images/agfvdlp4ksifmdnf0wfncz36s.png)       |
| [Compare Dates](/project_types/compare_dates.md)  | 3   | Two images are shown, the upper picture shows a scene before e.g. a disaster, while the lower picture shows the scene afterwards. By tapping you can classify the scene as *yes*, *maybe* or *bad_imagery*. Project managers can define which objects to look for, e.g. "buildings". Furthermore, they can specify the tile server of the background satellite imagery, e.g. "bing" or a custom tile server. | ![](/assets/project_types/project_types/images/gbaxwx4wnsjdfcshyh3z7exdw.png) |
| [Assess Images](/project_types/assess_images.md)      | 10  | An image with a bounding box (annotation) surrounding the class set by the project manager is displayed. The same image can have multiple annotations, in which case the same image is displayed again but with a different annotation. Users select one of the custom options set, usually 'Yes', 'No', 'Maybe'.                                                                                            | ![](/assets/project_types/project_types/images/xh147pt4dbuniejyi6maffrd9.png)                                                 |
| [Check Completeness](/project_types/check_completeness.md) | 4   | Similar to the Find Features project type but with an addition of an overlay raster or vector layer. Currently, MapSwipe mobile app only supports raster layer while MapSwipe4Web support both. You can call it a mix of Find Features and Validate Footprints in a nutshell.                                                                                                                                | ![](/assets/project_types/project_types/images/qu4oy95b0hot07i6lei6189qj.png) |
| [View Streets](/project_types/view_streets.md)                                        | 7   | An imagery version of the Validate Footprint project type where users can look for a specific feature (set by the project managers) in a set of Mapillary images.                                                                                                                                                                                                                                            | ![](/assets/project_types/project_types/images/k9nzk7129lqaqztgp6d67mzad.png) |


## Data Model
This way of formulating the overall crowdsourcing challenge and it's subcomponents shapes the **data model** we use.

Below you can see the structure on the example of a Find Features project type. The project manager supplies a bounding polygon, which is then divided into multiple groups, which are in turn divided into multiple tasks. Results are always bound to a task and what a result means differs by project type.

![](/assets/project_types/project_types/mapswipe_data_model.png)

With the revamp, as a project manager you have to care about the project. The information you provide through the **Manager Dashboard** will be used to set up your project. You should provide the following information.

### Projects
In the new architecture, the project can be created in a single sitting instead of having to create a draft and make active later. The **project** holds all information which are needed for the MapSwipe app such as progress and number of users who contributed.
A project consists of several groups.

| Parameter                           | Description                                                                                                                                         |
|-------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------|
| *Basic Information*                 |                                                                                                                                                     |
| **Name**                            | The name of your project (25 chars max)                                                                                                             |
| **Look For**                        | What should the users look for (e.g. buildings, cars, trees)? (15 chars max).                                                                       |
| **Project Type**                    | Is `1` for all Find projects.                                                                                                                 |
| **Direct Image Link**               | An url to an image. Make sure you have the rights to use this image. It should end with .jpg or .png.                                               |
| **Project Details**                 | The description for your project. (3-5 sentences).                                                                                                  |
| **Verification Number**             | How many people do you want to see every tile before you consider it finished? (default is 3 - more is recommended for harder tasks, but this will also make project take longer) |
| **Group Size**                      | How big should a mapping session be? Group size refers to the number of tasks per mapping session.                                                  |
| **progress**                        |                                                                                                                                                     |
| **isFeatured**                      | If true the project will appear bigger in the app.                                                                                                  |
| **projectId**                       | ID of the project.                                                                                                                                  |
| **contributorCount**                | How many volunteers contributed.                                                                                                                    |
| **resultCount**                     |                                                                                                                                                     |
| **numberOfTasks**                   | Number of tasks in project.                                                                                                                         |
| **status**                          | Active vs inactive.                                                                                                                                 |
| *Project Type Specific Information* | There will be varying parameters defined by the individual project types. You can find this information at the page for each project type.          |

### Groups
The **groups** are an intermediary between projects and tasks.
Each group belongs to a single project and consists of several tasks.

Single MapSwipe projects can contain up to several hundred thousand tasks.
This can pose a challenge to fast and performant communication between clients and server if many volunteers contribute data at the same time.
Therefore, groups have been introduced to reduce the amount of client requests on the backend server.

Groups consists of several tasks, that will be shown to the user in one mapping session.
They are the key to distribute tasks to MapSwipe users in a way that we can ensure that everything gets mapped as often as required in an efficient manner.

| Parameter                           | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
|-------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| *Basic Information*                 |                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| groupId                             | ID of the group.                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| numberOfTasks                       | How many tasks are in each group.                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| projectId                           | ID of the project the group belongs to.                                                                                                                                                                                                                                                                                                                                                                                                                           |
| finishedCount                       | Once a group has been completely mapped by a volunteer the completed count of the corresponding group will be raised by one. The completed count of the group is used to assess the overall progress of each project. <br/>For doing so the completed count is compared to the redundancy required (see Table 2). During the mapping process groups will be served in ascending completed count order. Thus, groups with low completed count will be served first |
| requiredCount                       | How many volunteers have to map a group.                                                                                                                                                                                                                                                                                                                                                                                                                          |
| *Project Type Specific Information* | There will be varying parameters defined by the individual project types. You can find this information at the page for each project type.                                                                                                                                                                                                                                                                                                                        |

### Tasks
The **tasks** are the smallest component in our data model.
Each task formulates an easy and quick to solve mapping challenge.
In many cases this challenge can be put into a simple question, e.g. *Can you see a building in this satellite imagery tile*.
Tasks always belong to a specific group and project.

Tasks are usually gzip compressed on firebase to save space. That is why this information is not readable by humans in firebase.

| Parameter                           | Description                                                                                                                                |
|-------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| *Basic Information*                 |                                                                                                                                            |
| **taskId**                          | ID of the task.                                                                                                                            |
| **groupId**                         | ID of the group the task belongs to.                                                                                                       |
| **projectId**                       | ID of the project the task belongs to.                                                                                                     |
| *Project Type Specific Information* | There will be varying parameters defined by the individual project types. You can find this information at the page for each project type. |


### Results
The **results** hold the information you wanted in the very beginning.
For each task you will receive several results by different users.
A result is the simple answer to your initial question.
For instance, it's a simple "yes" to the question "can you see a building in this satellite imagery tile".

| Parameter | Description |
|-----------|-------------|
| timestamp |             |
| startTime |             |
| endTime   |             |
| result    |             |


### Users
The **users** provide the results to your tasks.
They are the key to solve your mapping challenge.
For each user we generate mapping related statistics, e.g. the number of projects a user has been worked on.

| Parameter                 | Description |
| ------------------------- | ----------- |
| created                   |             |
| projectContributionsCount |             |
| groupContributionCount    |             |
| taskContributionCount     |             |
| timeSpentMapping          |             |
| username                  |             |
