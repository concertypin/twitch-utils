import os
import requests


# noinspection PyDefaultArgument
def make_token(
    client_id: str = os.environ.get("TWITCH_CLIENT_ID"),
    client_secret: str = os.environ.get("TWITCH_CLIENT_SECRET"),
    scopes: list = ["chat:read", "chat:edit"],
):
    # Make a twitch token.
    # client_id and client_secret are given as environment variables.
    # scopes are given as list.

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
        "scope": " ".join(scopes),
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


def ban(
    maguni_name: str,
    channelname: str,
    token_username: str,
    reason: str = "",
    token: str = os.environ.get("TWITCH_TOKEN"),
    client_id: str = os.environ.get("TWITCH_CLIENT_ID"),
):
    # Make maguni_name ban in channelname's twitch stream.
    # twitch token might be given as environment variable.
    # If not, it will be given as argument.
    # token_username is token owner's username.

    if token is None:
        raise TypeError(
            "token must be in TWITCH_TOKEN environment variable or in arguments."
        )
    if client_id is None:
        raise TypeError(
            "client_id must be in TWITCH_CLIENT_ID environment variable or in arguments."
        )

    url = "https://api.twitch.tv/helix/moderation/bans"
    query_params = {"broadcaster_id": channelname, "moderator_id": token_username}
    headers = {
        "Authorization": f"Bearer {token}",
        "Client-ID": client_id,
        "Content-Type": "application/json",
    }
    data = {"user_id": maguni_name, "reason": reason}

    r = requests.post(url, params=query_params, headers=headers, data=data)
    return r
