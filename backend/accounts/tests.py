"""
Automated checks for the accounts API. Run them with:

    python manage.py test

Each test uses a fresh, temporary database, so your real accounts are never touched.
"""
import json
from io import BytesIO
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, TestCase, override_settings

User = get_user_model()


class AccountApiTests(TestCase):
    def setUp(self):
        # enforce_csrf_checks=True makes the test behave like a real browser.
        self.client = Client(enforce_csrf_checks=True)
        self.client.get("/api/csrf/")
        # self.token = self.client.cookies["csrftoken"].value
        # Claude suggested removing the above line, commenting it out in case it is needed later.
    def post(self, url, data):
        return self.client.post(
            url, 
            json.dumps(data), 
            content_type="application/json", 
            # HTTP_X_CSRFTOKEN=self.token
            # Claude suggested replacing the above line with the following line.
            HTTP_X_CSRFTOKEN=self.client.cookies["csrftoken"].value
        )

    def signup(self, email="sam@example.com", password="Backlog-Hero-42", username="sam"):
        return self.post("/api/signup/", {"email": email, "password": password, "username": username})

    def test_signup_creates_account_and_signs_in(self):
        response = self.signup()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["user"]["username"], "sam")
        user = User.objects.get(email="sam@example.com")
        self.assertNotEqual(user.password, "Backlog-Hero-42")  # stored hashed
        self.assertTrue(user.check_password("Backlog-Hero-42"))
        self.assertEqual(self.client.get("/api/me/").json()["user"]["email"], "sam@example.com")

    def test_duplicate_email_rejected(self):
        self.signup()
        response = self.signup(email="SAM@example.com", username="other")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 1)

    def test_weak_password_rejected(self):
        response = self.signup(password="123")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(User.objects.count(), 0)

    def test_login_logout(self):
        self.signup()
        self.post("/api/logout/", {})
        self.assertIsNone(self.client.get("/api/me/").json()["user"])

        response = self.post("/api/login/", {"email": "sam@example.com", "password": "Backlog-Hero-42"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.client.get("/api/me/").json()["user"]["username"], "sam")

    def test_wrong_password_rejected(self):
        self.signup()
        self.post("/api/logout/", {})
        response = self.post("/api/login/", {"email": "sam@example.com", "password": "wrong-password"})
        self.assertEqual(response.status_code, 401)
        self.assertIsNone(self.client.get("/api/me/").json()["user"])

    def test_post_without_csrf_token_rejected(self):
        response = self.client.post(
            "/api/login/", json.dumps({"email": "a@b.com", "password": "x"}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)


class GameSearchApiTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client.force_login(User.objects.create_user(username="searcher", password="password"))

    def test_search_requires_sign_in(self):
        self.client.logout()

        response = self.client.get("/api/games/search/?q=zelda")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["error"], "Sign in to search games.")

    def test_search_requires_query(self):
        response = self.client.get("/api/games/search/")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["error"], "Enter a game title to search.")

    @override_settings(IGDB_CLIENT_ID="", IGDB_CLIENT_SECRET="")
    def test_search_reports_missing_igdb_credentials(self):
        response = self.client.get("/api/games/search/?q=zelda")

        self.assertEqual(response.status_code, 503)
        self.assertEqual(response.json()["error"], "IGDB is not configured.")

    @override_settings(IGDB_CLIENT_ID="client-id", IGDB_CLIENT_SECRET="client-secret")
    @patch("accounts.views.urllib.request.urlopen")
    def test_search_returns_igdb_games_with_backlog_defaults(self, urlopen):
        urlopen.side_effect = [
            BytesIO(b'{"access_token":"test-token","expires_in":3600}'),
            BytesIO(
                json.dumps(
                    [
                        {
                            "id": 42,
                            "name": "Example Game",
                            "genres": [{"name": "Adventure"}],
                            "platforms": [{"name": "PC"}],
                            "cover": {
                                "url": "//images.igdb.com/igdb/image/upload/t_thumb/co123.jpg"
                            },
                            "rating": 86,
                        }
                    ]
                ).encode()
            ),
        ]

        response = self.client.get("/api/games/search/?q=example")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["games"],
            [
                {
                    "id": 42,
                    "title": "Example Game",
                    "genre": "Adventure",
                    "platform": "PC",
                    "progress": 0,
                    "hours": 0,
                    "status": "Backlog",
                    "image": "https://images.igdb.com/igdb/image/upload/t_cover_big/co123.jpg",
                    "color": "#6f4be5",
                    "score": 4.3,
                }
            ],
        )
