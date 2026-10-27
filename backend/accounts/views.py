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

from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET, require_POST

User = get_user_model()


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
