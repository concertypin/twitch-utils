import os
import requests


# noinspection PyDefaultArgument
def make_oauth_token(
    client_id: str = os.environ.get("TWITCH_CLIENT_ID"),
    client_secret: str = os.environ.get("TWITCH_CLIENT_SECRET"),
    scope: dict = ["user_read"],
) -> dict:
    # Make a twitch oauth token.
    # client_id is given as environment variable.

    if client_id is None:
        raise TypeError(
            "client_id must be in TWITCH_CLIENT_ID environment variable or in arguments."
        )

    if client_secret is None:
        raise TypeError(
            "client_secret must be in TWITCH_CLIENT_SECRET environment variable or in arguments."
        )

    url = "https://id.twitch.tv/oauth2/token"
    query_params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
        "scope": " ".join(scope),
    }

    r = requests.post(url, params=query_params)
    return r.json()


def validate_token(
    token: str = os.environ.get("TWITCH_TOKEN"),
    client_id: str = os.environ.get("TWITCH_CLIENT_ID"),
) -> dict:
    # Validate twitch token.

    if token is None:
        raise TypeError(
            "token must be in TWITCH_TOKEN environment variable or in arguments."
        )
    if client_id is None:
        raise TypeError(
            "client_id must be in TWITCH_CLIENT_ID environment variable or in arguments."
        )

    url = "https://id.twitch.tv/oauth2/validate"
    headers = {"Authorization": f"Bearer {token}"}

    r = requests.get(url, headers=headers)
    return r.json()
