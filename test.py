import os
import unittest


class MyTestCase(unittest.TestCase):
    def test_token(self):
        import twitch_utils.auth as auth

        d = auth.Auth("heisenberg_cat")
        d.make_oauth_token()
        self.assertEqual(
            os.environ["TWITCH_CLIENT_ID"], d.validate_token()["client_id"]
        )  # add assertion here


if __name__ == "__main__":
    unittest.main()
