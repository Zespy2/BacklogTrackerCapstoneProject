
import json

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .services import recommend_game


@require_POST
def game_recommendation(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "Invalid JSON request."},
            status=400,
        )

    if not isinstance(data, dict):
        return JsonResponse(
            {"error": "Request must be a JSON object."},
            status=400,
        )

    games = data.get("games", [])
    favorite_genres = data.get("favorite_genres", [])

    if not isinstance(games, list):
        return JsonResponse(
            {"error": "Games must be a list."},
            status=400,
        )

    if not isinstance(favorite_genres, list):
        return JsonResponse(
            {"error": "Favorite genres must be a list."},
            status=400,
        )

    if len(games) > 100:
        return JsonResponse(
            {"error": "Maximum of 100 games allowed."},
            status=400,
        )

    result = recommend_game(games, favorite_genres)

    return JsonResponse(result)
