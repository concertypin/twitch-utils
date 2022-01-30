import os
import requests

# Usage:
# import twitch_utils.auth
# import twitch_utils.user
# auth_data = twitch_utils.auth.Auth("YourUsername", "YourClientID", "YourClientSecret")
# twitch_utils.user.whatYouWantToRun(params..., auth_data)


class Auth:
    def __init__(
        self,
        username: str,
        client_id: str = os.environ.get("TWITCH_CLIENT_ID"),
        client_secret: str = os.environ.get("TWITCH_CLIENT_SECRET"),
    ):
        if (client_id is None) or (client_secret is None):
            raise ValueError(
                "Client ID and Client Secret must be in environment variables or passed as arguments."
            )
        self.username = username
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = None
        self.refresh_token = None
        self.expires_in = None

    # noinspection PyDefaultArgument
    def make_oauth_token(self, scope: dict = ["user_read"]) -> dict:
        # Make a twitch oauth token.
        # client_id and client_secret will be used as class variables.
        # Twitch docs: https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/
        client_id = self.client_id
        client_secret = self.client_secret

        url = "https://id.twitch.tv/oauth2/token"
        query_params = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
            "scope": " ".join(scope),
        }

        r = requests.post(url, params=query_params)
        self.access_token = r.json()["access_token"]
        return r.json()

    def validate_token(self) -> dict:
        # Validate twitch token.
        # token and client_id will be used as class variables.
        # Twitch docs: https://dev.twitch.tv/docs/authentication/getting-tokens-oauth/
        token = self.access_token

        url = "https://id.twitch.tv/oauth2/validate"
        headers = {"Authorization": f"Bearer {token}"}

        r = requests.get(url, headers=headers)
        return r.json()
