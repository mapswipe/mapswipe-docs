# /// script
# dependencies = [
#   "httpx",
#   "python-dotenv",
#   "python-ulid>=3.0.0",
#   "typing-extensions",
#   "colorlog",
# ]
# ///

# NOTE: Please read ./README.md

import json
import typing
import httpx
import logging
import colorlog
from dotenv import dotenv_values
from ulid import ULID

config = dotenv_values(".env")


def logging_init():
    handler = colorlog.StreamHandler()
    handler.setFormatter(
        colorlog.ColoredFormatter(
            "%(log_color)s[%(levelname)s]%(reset)s %(message)s",
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        )
    )

    logger = colorlog.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger


logger = logging_init()


# Define the GraphQL query
class Query:
    ME_OP_NAME = "Me"
    ME = """
        query Me {
          me {
            id
            displayName
          }
        }
    """

    PUBLIC_PROJECTS_OP_NAME = "PublicProjectsList"
    PUBLIC_PROJECTS = """
        query PublicProjectsList($filters: ProjectFilter = {}) {
          publicProjects(filters: $filters) {
            totalCount
            results {
              id
              firebaseId
              name

              exportAggregatedResults {
                id
                file {
                  url
                }
              }
              exportUsers {
                id
                file {
                    url
                }
              }
              exportTasks {
                id
                file {
                    url
                }
              }
              exportResults {
                id
                file {
                    url
                }
              }
              exportModerateToHighAgreementYesMaybeGeometries {
                id
                file {
                    url
                }
              }
              exportHotTaskingManagerGeometries {
                id
                file {
                    url
                }
              }
              exportHistory {
                id
                file {
                    url
                }
              }
              exportGroups {
                id
                file {
                    url
                }
              }
              exportAreaOfInterest {
                id
                file {
                    url
                }
              }
              exportAggregatedResultsWithGeometry {
                id
                file {
                    url
                }
              }

            }
          }
        }
        """

    PROJECTS_OP_NAME = "ProjectsList"
    PROJECTS = """
        query ProjectsList {
          projects {
            totalCount
            results {
              id
              firebaseId
              name

              exportAggregatedResults {
                id
                file {
                  url
                }
              }
              exportUsers {
                id
                file {
                    url
                }
              }
              exportTasks {
                id
                file {
                    url
                }
              }
              exportResults {
                id
                file {
                    url
                }
              }
              exportModerateToHighAgreementYesMaybeGeometries {
                id
                file {
                    url
                }
              }
              exportHotTaskingManagerGeometries {
                id
                file {
                    url
                }
              }
              exportHistory {
                id
                file {
                    url
                }
              }
              exportGroups {
                id
                file {
                    url
                }
              }
              exportAreaOfInterest {
                id
                file {
                    url
                }
              }
              exportAggregatedResultsWithGeometry {
                id
                file {
                    url
                }
              }

            }
          }
        }
        """

    ORGANIZATIONS_OP_NAME = "Organizations"
    ORGANIZATIONS = """
        query Organizations {
          organizations {
            totalCount
            results {
              id
              name
            }
          }
        }
    """

    CREATE_DRAFT_PROJECTS_OP_NAME = "NewDraftProject"
    CREATE_DRAFT_PROJECTS = """
        mutation NewDraftProject($data: ProjectCreateInput!) {
            createProject(data: $data) {
                ... on OperationInfo {
                  __typename
                  messages {
                    code
                    field
                    kind
                    message
                  }
                }
                ... on ProjectTypeMutationResponseType {
                  errors
                  ok
                  result {
                    id
                    firebaseId
                  }
                }
            }
        }
    """

    CREATE_PROJECT_ASSET_OP_NAME = "CreateProjectAsset"
    CREATE_PROJECT_ASSET = """
        mutation CreateProjectAsset($data: ProjectAssetCreateInput!) {
          createProjectAsset(data: $data) {
            ... on ProjectAssetTypeMutationResponseType {
              errors
              ok
              result {
                id
                file {
                  name
                  url
                }
              }
            }
          }
        }
    """


class MapSwipeApiClient:
    # Set the base URL
    BASE_URL = config["BACKEND_URL"]
    CSRFTOKEN_KEY = config["CSRFTOKEN_KEY"]
    MANAGER_URL = config["MANAGER_URL"]

    ENABLE_AUTHENTICATION = (
        config.get("ENABLE_AUTHENTICATION", "false").lower() == "true"
    )
    FB_AUTH_URL = config.get("FB_AUTH_URL")

    # Your web-app login credential
    FB_USERNAME = config.get("FB_USERNAME")
    FB_PASSWORD = config.get("FB_PASSWORD")

    def __enter__(self):
        self.client = httpx.Client(base_url=self.BASE_URL, timeout=10.0)

        # For CSRF
        health_resp = self.client.get("/health-check/")
        health_resp.raise_for_status()

        if self.ENABLE_AUTHENTICATION:
            self.login_with_firebaes()

        csrf_token = self.client.cookies.get(self.CSRFTOKEN_KEY)
        self.headers = {
            # Required for CSRF verification
            "x-csrftoken": csrf_token,
            "origin": self.MANAGER_URL,
        }
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.client.close()
        return False  # If True, suppresses exceptions

    def login_with_firebaes(self):
        logger.info("Logging using firebase auth")
        resp = httpx.post(
            self.FB_AUTH_URL,
            headers={
                "origin": self.MANAGER_URL,
            },
            json={
                "returnSecureToken": True,
                "email": self.FB_USERNAME,
                "password": self.FB_PASSWORD,
                "clientType": "CLIENT_TYPE_WEB",
            },
        )
        resp.raise_for_status()

        idToken = resp.json()["idToken"]

        resp = self.client.post(
            "/firebase-auth/",
            json={
                "token": idToken,
            },
        )
        resp.raise_for_status()

    def graphql_request_with_files(
        self,
        operation_name: str,
        query: str,
        *,
        files: dict[typing.Any, typing.Any],
        map: dict[typing.Any, typing.Any],
        variables: dict[typing.Any, typing.Any] | None = None,
    ):
        # Request type: form data
        graphql_resp = self.client.post(
            "/graphql/",
            headers=self.headers,
            files=files,
            data={
                "operations": json.dumps(
                    {
                        "query": query,
                        "variables": variables,
                    },
                ),
                "map": json.dumps(map),
            },
        )

        if not (200 <= graphql_resp.status_code < 300):
            logger.error("Error: %s", graphql_resp.text)
        graphql_resp.raise_for_status()

        return graphql_resp.json()

    def graphql_request(
        self,
        operation_name: str,
        query: str,
        variables: dict[typing.Any, typing.Any] | None = None,
    ):
        payload = {
            "operationName": operation_name,
            "query": query,
            "variables": variables,
        }

        graphql_resp = self.client.post(
            "/graphql/",
            headers=self.headers,
            json=payload,
        )

        if not (200 <= graphql_resp.status_code < 300):
            logger.error("Error: %s", graphql_resp.text)
        graphql_resp.raise_for_status()

        return graphql_resp.json()

    def create_draft_project(self, params):
        resp = self.graphql_request(
            Query.CREATE_DRAFT_PROJECTS_OP_NAME,
            Query.CREATE_DRAFT_PROJECTS,
            {"data": params},
        )

        if errors := resp.get("errors"):
            logger.error("Failed to create new project: %s", errors)
            return None

        if errors := resp["data"]["createProject"].get("messages"):
            logger.error("Failed to create new project: %s", errors)
            return None

        if errors := resp["data"]["createProject"].get("errors"):
            logger.error("Failed to create new project: %s", errors)
            return None

        return resp["data"]["createProject"]["result"]["id"]

    def create_project_asset(
        self,
        *,
        project_file,
        params,
    ):
        resp = self.graphql_request_with_files(
            Query.CREATE_PROJECT_ASSET_OP_NAME,
            Query.CREATE_PROJECT_ASSET,
            files={
                "projectFile": project_file,
            },
            map={
                "projectFile": ["variables.data.file"],
            },
            variables={"data": params},
        )

        if errors := resp.get("errors"):
            logger.error("Failed to create project asset: %s", errors)
            return None

        if errors := resp["data"]["createProjectAsset"].get("messages"):
            logger.error("Failed to create project asset: %s", errors)
            return None

        if errors := resp["data"]["createProjectAsset"].get("errors"):
            logger.error("Failed to create project asset: %s", errors)
            return None

        return resp["data"]["createProjectAsset"]["result"]["id"]


def run():
    with MapSwipeApiClient() as api_client:
        logger.info("Public endpoints")

        logger.info(
            "%s: %s",
            Query.PUBLIC_PROJECTS_OP_NAME,
            api_client.graphql_request(
                Query.PUBLIC_PROJECTS_OP_NAME,
                Query.PUBLIC_PROJECTS,
                variables={
                    "filters": {
                        "status": {
                            "exact": "FINISHED",
                        }
                    }
                },
            ),
        )

        logger.info("Private endpoints")
        me_info = api_client.graphql_request(Query.ME_OP_NAME, Query.ME)["data"]["me"]
        if not me_info:
            raise Exception("Not logged in.... :(")
        logger.info("%s: %s", Query.ME_OP_NAME, me_info)

        organization_id = api_client.graphql_request(
            Query.ORGANIZATIONS_OP_NAME,
            Query.ORGANIZATIONS,
        )["data"]["organizations"]["results"][0]["id"]

        logger.info(
            "%s: %s",
            Query.PUBLIC_PROJECTS_OP_NAME,
            api_client.graphql_request(Query.PROJECTS_OP_NAME, Query.PROJECTS),
        )

        new_project_client_id = str(ULID())
        new_project_topic_name = "Test - Building Validation - 8"

        logger.warning(
            "You are about to create projects in %s. This may modify the environment.",
            api_client.BASE_URL,
        )
        confirmation = input('Proceed? Type "yes" to continue: ').strip().lower()
        if confirmation != "yes":
            logger.warning("Operation cancelled. No changes were made.")
            return None

        new_project_id = api_client.create_draft_project(
            {
                "clientId": new_project_client_id,
                "projectType": "VALIDATE",
                "region": "Nepal",
                "topic": new_project_topic_name,
                "description": "Validate building footprints",
                "projectInstruction": "Validate building footprints",
                "lookFor": "buildings",
                "projectNumber": 1000,
                "requestingOrganization": organization_id,
                "additionalInfoUrl": "fair-dev.hotosm.org",
                "team": None,
            }
        )
        assert new_project_id is not None

        logger.info("%s: %s", "Create Draft Project", new_project_id)

        with open("./sample_image.png", "rb") as image_file:
            new_project_asset_client_id = str(ULID())
            new_project_asset = api_client.create_project_asset(
                project_file=image_file,
                params={
                    "inputType": "COVER_IMAGE",
                    "clientId": new_project_asset_client_id,
                    "project": new_project_id,
                },
            )

            logger.info("%s: %s", "Create Project Asset", new_project_asset)


run()
