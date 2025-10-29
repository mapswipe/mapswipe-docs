# /// script
# dependencies = [
#   "httpx",
#   "python-dotenv",
# ]
# ///

# NOTE: Please read ./README.md

import httpx
import logging
from dotenv import dotenv_values

logger = logging.getLogger(__name__)
config = dotenv_values(".env")


# Define the GraphQL query
class Query:

    ME = """
        query MyQuery {
          me {
            id
            displayName
          }
        }
    """

    PUBLIC_PROJECTS = """
        query MyQuery($filters: ProjectFilter = {}) {
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

    PROJECTS = """
        query MyQuery {
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

class MapswipeApi:
    # Set the base URL
    BASE_URL = config["BACKEND_URL"]
    CSRFTOKEN_KEY = config["CSRFTOKEN_KEY"]
    MANAGER_URL = config["MANAGER_URL"]

    ENABLE_AUTHENTICATION = config.get("ENABLE_AUTHENTICATION", "false").lower() == "true"
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
            "content-type": "application/json",
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

    def graphql_request(self, query, variables = None):
        graphql_resp = self.client.post(
            "/graphql/",
            headers=self.headers,
            json={
                "query": query,
                "variables": variables,
            },
        )

        graphql_resp.raise_for_status()

        return graphql_resp.json()


with MapswipeApi() as api:
    print('Public endpoints')

    print(
        api.graphql_request(
            Query.PUBLIC_PROJECTS,
            variables={
                "filters": {
                    "status": {
                        "exact": "FINISHED",
                    }
                }
            },
        )
    )

    print('Private endpoints')
    print(api.graphql_request(Query.ME))

    print(api.graphql_request(Query.PROJECTS))
