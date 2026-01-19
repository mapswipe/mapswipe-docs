## Background

This script is provided as an example for interacting with the MapSwipe backend.

> [!CAUTION]
> Ongoing updates to the backend might render this script **out-of-date**.

## Real-world usage

- https://github.com/hotosm/fAIr/blob/develop/backend/core/mapswipe_client.py

## Getting started

> [!NOTE]
> You will need Manager account credentials to run this script.

- Create `.env` file.
- Define the following variables:
    - `MANAGER_URL`: URL for Manager Dashboard
    - `BACKEND_URL`: URL for Backend
    - `CSRFTOKEN_KEY`: CSRF Token Key
    - `ENABLE_AUTHENTICATION`
    - `FB_AUTH_URL`: Authentication URL
    - `FB_USERNAME`: Manager account username
    - `FB_PASSWORD`: Manager account password
- For `FB_AUTH_URL`,
    - Sign-in on the Manager Dashboard and open Dev Console.
    - Look for the URL which starts with https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword
      <img width="1305" height="228" alt="image" src="https://github.com/user-attachments/assets/332e6673-f0e3-48c4-8420-13ef5d648f21" />

### Alpha Instance

> [!CAUTION]
> The alpha instance is running inside Togglecorp's domain for internal testing.

Your final `.env` for alpha instance should look like this:

```dotenv
MANAGER_URL=https://manager-2.mapswipe.dev.togglecorp.com
BACKEND_URL=https://backend-2.mapswipe.dev.togglecorp.com
CSRFTOKEN_KEY=MAPSWIPE-ALPHA-2-CSRFTOKEN

ENABLE_AUTHENTICATION=true
FB_AUTH_URL=https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Your web-app login credential
FB_USERNAME=me@example.com
FB_PASSWORD=my-very-good-password
```

### Staging Instance

Your final `.env` for staging instance should look like this:

```dotenv
MANAGER_URL=https://managers-stage.mapswipe.org
BACKEND_URL=https://backend-stage.mapswipe.org
CSRFTOKEN_KEY=MAPSWIPE-STAGE-CSRFTOKEN

ENABLE_AUTHENTICATION=true
FB_AUTH_URL=https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Your web-app login credential
FB_USERNAME=me@example.com
FB_PASSWORD=my-very-good-password
```

### Production Instance

Your final `.env` for production instance should look like this:

```dotenv
MANAGER_URL=https://managers.mapswipe.org
BACKEND_URL=https://backend.mapswipe.org
CSRFTOKEN_KEY=MAPSWIPE-PROD-CSRFTOKEN

ENABLE_AUTHENTICATION=false
FB_AUTH_URL=https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
# Your web-app login credential
FB_USERNAME=me@example.com
FB_PASSWORD=my-very-good-password
```

## Running the script

Run the example script using uv

```bash
uv run run.py
```

> [!NOTE]
> To install uv, visit https://docs.astral.sh/uv/getting-started/installation/
