
import json
import os
from pathlib import Path

from google import genai


PROMPT_PATH = (
    Path(__file__).resolve().parent.parent
    / "prompts"
    / "recommendation_v1.txt"
)


def fallback_recommendation(games):
    """Return a safe recommendation without calling Gemini."""
    if not games:
        return {
            "game": None,
            "reason": "Add games to your backlog to get recommendations.",
            "source": "fallback",
        }

    game = games[0]

    return {
        "game": game["title"],
        "reason": "AI is unavailable. Try this game from your backlog.",
        "source": "fallback",
    }


def recommend_game(games, favorite_genres=None):
    """Recommend one backlog game using Gemini, with a safe fallback."""
    if not games:
        return fallback_recommendation(games)

    # Only use games with valid, nonempty titles.
    valid_games = [
        game
        for game in games
        if isinstance(game, dict)
        and isinstance(game.get("title"), str)
        and game["title"].strip()
    ]

    if not valid_games:
        return fallback_recommendation([])

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return fallback_recommendation(valid_games)

    try:
        prompt = PROMPT_PATH.read_text(encoding="utf-8")

        payload = {
            "games": valid_games,
            "favorite_genres": favorite_genres or [],
        }

        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model=os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
            contents=prompt + "\n\nUser backlog data:\n"
            + json.dumps(payload),
        )

        result = json.loads(response.text)

        if not isinstance(result, dict):
            raise ValueError("AI response must be a JSON object")

        game_title = result.get("game")
        reason = result.get("reason")

        if not isinstance(game_title, str):
            raise ValueError("Invalid game title")

        if not isinstance(reason, str) or not reason.strip():
            raise ValueError("Invalid explanation")

        allowed_titles = {
            game["title"].strip().casefold(): game["title"]
            for game in valid_games
        }

        matched_title = allowed_titles.get(game_title.strip().casefold())

        if not matched_title:
            raise ValueError("AI recommended a game outside the backlog")

        return {
            "game": matched_title,
            "reason": reason.strip(),
            "source": "gemini",
        }

    except (Exception):
        # Includes API errors, timeouts, and malformed AI output.
        return fallback_recommendation(valid_games)
