"""
The sign-in / sign-up API.

The React site sends JSON to these addresses and gets JSON back. Signing in
uses Django's normal session system: after a successful login, Django sets a
cookie in the browser so later requests know who the user is.

Every POST must include a CSRF token (a security measure against other
websites submitting forms as your users). The React code gets one from
/api/csrf/ and sends it back in the X-CSRFToken header.
"""
import json
import logging
import urllib.error
import urllib.parse
import urllib.request

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.password_validation import validate_password
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

User = get_user_model()
logger = logging.getLogger(__name__)


def user_data(user):
    """The account details we send to the React site (never the password)."""
    return {"id": user.id, "username": user.username, "email": user.email}


def read_json(request):
    """Read the JSON body the React site sent. Returns {} if it's missing or invalid."""
    try:
        data = json.loads(request.body or b"{}")
    except (json.JSONDecodeError, UnicodeDecodeError):
        return {}
    return data if isinstance(data, dict) else {}


def error(message, status=400):
    return JsonResponse({"error": message}, status=status)


@require_GET
@ensure_csrf_cookie
def csrf(request):
    """GET /api/csrf/ - gives the browser a CSRF cookie to use on later POSTs."""
    return JsonResponse({"ok": True})


@require_GET
def me(request):
    """GET /api/me/ - who is signed in right now? (user is null if nobody)."""
    if request.user.is_authenticated:
        return JsonResponse({"user": user_data(request.user)})
    return JsonResponse({"user": None})


@require_POST
def signup(request):
    """POST /api/signup/ with {email, password, username} - create an account."""
    data = read_json(request)
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))
    username = str(data.get("username", "")).strip()

    if not email or not password or not username:
        return error("Please fill in your email, password and username.")

    try:
        validate_email(email)
    except ValidationError:
        return error("Please enter a valid email address.")

    if len(username) > 150:
        return error("Usernames can be at most 150 characters.")

    if User.objects.filter(email__iexact=email).exists():
        return error("An account with that email already exists.")

    if User.objects.filter(username__iexact=username).exists():
        return error("That username is taken. Try another one.")

    # Check the password against the rules in settings.AUTH_PASSWORD_VALIDATORS
    # (at least 8 characters, not too common, not all numbers, not too similar
    # to the username or email).
    try:
        validate_password(password, user=User(username=username, email=email))
    except ValidationError as exc:
        return error(" ".join(exc.messages))

    # create_user hashes the password before saving it to the database.
    user = User.objects.create_user(username=username, email=email, password=password)
    login(request, user)
    return JsonResponse({"user": user_data(user)}, status=201)


@require_POST
def login_view(request):
    """POST /api/login/ with {email, password} - sign in."""
    data = read_json(request)
    email = str(data.get("email", "")).strip()
    password = str(data.get("password", ""))

    if not email or not password:
        return error("Please enter your email and password.")

    # Django signs people in by username, so look up the account by email
    # first. We give the same message whether the email or the password was
    # wrong, so nobody can use this form to find out who has an account.
    account = User.objects.filter(email__iexact=email).first()
    user = None
    if account is not None:
        user = authenticate(request, username=account.username, password=password)

    if user is None:
        return error("Incorrect email or password.", status=401)

    login(request, user)
    return JsonResponse({"user": user_data(user)})


@require_POST
def logout_view(request):
    """POST /api/logout/ - sign out."""
    logout(request)
    return JsonResponse({"ok": True})

<<<<<<< HEAD
@require_POST
def delete_account(request):
    """POST /api/delete-account/ with {password} - permanently delete the signed-in account."""
    if not request.user.is_authenticated:
        return error("You need to be signed in to delete your account.", status=401)

    data = read_json(request)
    password = str(data.get("password", ""))

    # Ask for the password again so nobody can delete an account from a
    # computer that was just left signed in.
    if not request.user.check_password(password):
        return error("Incorrect password. Your account was not deleted.")

    user = request.user
    logout(request)
    user.delete()  # removes the row from the accounts table
    return JsonResponse({"ok": True})
=======

def igdb_access_token():
    cache_key = f"igdb_access_token:{settings.IGDB_CLIENT_ID}"
    token = cache.get(cache_key)
    if token:
        return token

    token_request = urllib.request.Request(
        "https://id.twitch.tv/oauth2/token",
        data=urllib.parse.urlencode(
            {
                "client_id": settings.IGDB_CLIENT_ID,
                "client_secret": settings.IGDB_CLIENT_SECRET,
                "grant_type": "client_credentials",
            }
        ).encode(),
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    with urllib.request.urlopen(token_request, timeout=10) as response:
        token_data = json.loads(response.read())

    if not isinstance(token_data, dict):
        raise ValueError("IGDB returned an invalid token response.")

    token = token_data.get("access_token")
    if not isinstance(token, str) or not token:
        raise ValueError("IGDB returned an invalid access token.")

    expires_in = token_data.get("expires_in", 3600)
    timeout = max(60, int(expires_in) - 60)
    cache.set(cache_key, token, timeout=timeout)
    return token


def igdb_game_data(game):
    cover = game.get("cover")
    image = cover.get("url", "") if isinstance(cover, dict) else ""
    if not isinstance(image, str):
        image = ""
    if image.startswith("//"):
        image = f"https:{image}"
    image = image.replace("/t_thumb/", "/t_cover_big/")
    genres = game.get("genres")
    platforms = game.get("platforms")
    genre = next(
        (
            item["name"]
            for item in genres or []
            if isinstance(item, dict) and isinstance(item.get("name"), str)
        ),
        "Genre unavailable",
    )
    platform = next(
        (
            item["name"]
            for item in platforms or []
            if isinstance(item, dict) and isinstance(item.get("name"), str)
        ),
        "Platform unavailable",
    )
    rating = game.get("rating")

    result = {
        "id": game["id"],
        "title": game["name"],
        "genre": genre,
        "platform": platform,
        "progress": 0,
        "hours": 0,
        "status": "Backlog",
        "image": image,
        "color": "#6f4be5",
    }
    if isinstance(rating, (int, float)):
        result["score"] = round(rating / 20, 1)
    return result


@require_GET
def search_games(request):
    if not request.user.is_authenticated:
        return error("Sign in to search games.", status=401)

    query = " ".join(request.GET.get("q", "").split())
    if not query:
        return error("Enter a game title to search.")
    if len(query) > 100:
        return error("Search terms must be 100 characters or fewer.")
    if not settings.IGDB_CLIENT_ID or not settings.IGDB_CLIENT_SECRET:
        return error("IGDB is not configured.", status=503)

    escaped_query = query.replace("\\", "\\\\").replace('"', '\\"')
    igdb_query = (
        f'search "{escaped_query}"; '
        "fields id,name,genres.name,platforms.name,cover.url,rating; "
        "limit 20;"
    )

    try:
        token = igdb_access_token()
        games_request = urllib.request.Request(
            "https://api.igdb.com/v4/games",
            data=igdb_query.encode(),
            headers={
                "Client-ID": settings.IGDB_CLIENT_ID,
                "Authorization": f"Bearer {token}",
                "Content-Type": "text/plain",
            },
            method="POST",
        )
        with urllib.request.urlopen(games_request, timeout=10) as response:
            games_data = json.loads(response.read())
        if not isinstance(games_data, list):
            raise ValueError("IGDB returned an invalid games response.")
        games = [
            igdb_game_data(game)
            for game in games_data
            if isinstance(game, dict)
            and isinstance(game.get("id"), int)
            and isinstance(game.get("name"), str)
        ]
    except (
        urllib.error.URLError,
        TimeoutError,
        ValueError,
        json.JSONDecodeError,
        UnicodeDecodeError,
        KeyError,
        TypeError,
    ):
        logger.exception("IGDB game search failed.")
        return error("IGDB search is temporarily unavailable. Please try again.", status=502)

    return JsonResponse({"games": games})
>>>>>>> 4504baf (fuck it, try and maybe add api fuctionality hope this works)
