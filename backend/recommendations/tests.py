
import json
import os
from unittest.mock import MagicMock, patch

from django.test import SimpleTestCase

from .services import recommend_game


class RecommendationTests(SimpleTestCase):

    def setUp(self):
        self.games = [
            {"title": "Elden Ring"},
            {"title": "Stardew Valley"},
        ]

    @patch.dict(os.environ, {"GEMINI_API_KEY": ""})
    def test_missing_api_key_uses_fallback(self):
        result = recommend_game(self.games)

        self.assertEqual(result["source"], "fallback")
        self.assertEqual(result["game"], "Elden Ring")

    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake-test-key"})
    @patch("recommendations.services.genai.Client")
    def test_successful_gemini_response(self, mock_client):
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "game": "Stardew Valley",
            "reason": "A relaxing game to play next.",
        })

        mock_client.return_value.models.generate_content.return_value = (
            mock_response
        )

        result = recommend_game(self.games)

        self.assertEqual(result["source"], "gemini")
        self.assertEqual(result["game"], "Stardew Valley")

    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake-test-key"})
    @patch("recommendations.services.genai.Client")
    def test_api_failure_uses_fallback(self, mock_client):
        mock_client.return_value.models.generate_content.side_effect = (
            ConnectionError("Simulated API failure")
        )

        result = recommend_game(self.games)

        self.assertEqual(result["source"], "fallback")
        self.assertEqual(result["game"], "Elden Ring")

    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake-test-key"})
    @patch("recommendations.services.genai.Client")
    def test_timeout_uses_fallback(self, mock_client):
        mock_client.return_value.models.generate_content.side_effect = (
            TimeoutError("Simulated timeout")
        )

        result = recommend_game(self.games)

        self.assertEqual(result["source"], "fallback")

    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake-test-key"})
    @patch("recommendations.services.genai.Client")
    def test_invalid_json_uses_fallback(self, mock_client):
        mock_response = MagicMock()
        mock_response.text = "Not valid JSON"

        mock_client.return_value.models.generate_content.return_value = (
            mock_response
        )

        result = recommend_game(self.games)

        self.assertEqual(result["source"], "fallback")

    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake-test-key"})
    @patch("recommendations.services.genai.Client")
    def test_game_outside_backlog_uses_fallback(self, mock_client):
        mock_response = MagicMock()
        mock_response.text = json.dumps({
            "game": "Minecraft",
            "reason": "Try this game.",
        })

        mock_client.return_value.models.generate_content.return_value = (
            mock_response
        )

        result = recommend_game(self.games)

        self.assertEqual(result["source"], "fallback")
        self.assertIn(
            result["game"],
            ["Elden Ring", "Stardew Valley"],
        )

    @patch("recommendations.services.genai.Client")
    def test_empty_backlog_does_not_call_ai(self, mock_client):
        result = recommend_game([])

        self.assertEqual(result["source"], "fallback")
        self.assertIsNone(result["game"])
        mock_client.assert_not_called()
