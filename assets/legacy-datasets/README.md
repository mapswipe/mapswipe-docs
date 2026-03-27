## [projects.csv](./projects.csv)

> [!NOTE]
> Related discussion: https://mapswipe.slack.com/archives/C0HCW2CJJ/p1774445684627589

Exported project data from the legacy system, including:

* **project_old_id**: Legacy project identifier
* **tile_server_name**: Name of the associated tile server

## Query used for export

```sql
select
    project_id as project_old_id,
    project_type_specifics -> 'tileServer' -> 'name' as tile_server_name
from projects;
```
> [!NOTE]
> Run in legacy database
