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

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import JsonResponse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
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


    # Same message whether or not the email has an account, so nobody can use the
# "Forgot password?" form to find out who is signed up.
RESET_SENT_MESSAGE = "If an account uses that email, we've sent a link to reset your password."
RESET_LINK_INVALID = "This reset link is invalid or has expired. Please request a new one."


@require_POST
def forgot_password(request):
    """POST /api/forgot-password/ with {email} - email the user a password reset link."""
    data = read_json(request)
    email = str(data.get("email", "")).strip()

    if not email:
        return error("Please enter your email address.")

    user = User.objects.filter(email__iexact=email, is_active=True).first()
    if user is not None and user.has_usable_password():
        # uid = the user's id, encoded so it is safe to put in a link.
        # token = a one-time code made from the user's current password hash and
        # last login, so it stops working once the password changes. It also
        # expires after settings.PASSWORD_RESET_TIMEOUT seconds.
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        link = f"{settings.FRONTEND_URL}/reset-password?uid={uid}&token={token}"
        if settings.DEBUG:
            # The printed email wraps long lines and turns "=" into "=3D", which
            # breaks the link. Print a clean copy so it can be clicked while testing.
            print(f"\nPassword reset link for {user.email}:\n{link}\n", flush=True)
        try:
            send_mail(
                subject="Reset your Inventory password",
                message=(
                    f"Hi {user.username},\n\n"
                    f"Someone asked to reset the password for your Inventory account. "
                    f"To choose a new password, open this link:\n\n{link}\n\n"
                    f"The link works once and expires in "
                    f"{settings.PASSWORD_RESET_TIMEOUT // 60} minutes. "
                    f"If you didn't ask for this, you can ignore this email."
                ),
                from_email=None,  # uses settings.DEFAULT_FROM_EMAIL
                recipient_list=[user.email],
            )
        except Exception:
            # Log it for us, but don't show a different reply to the user.
            logger.exception("Could not send password reset email")

    return JsonResponse({"message": RESET_SENT_MESSAGE})


@require_POST
def reset_password(request):
    """POST /api/reset-password/ with {uid, token, new_password} - set a new password."""
    data = read_json(request)
    uid = str(data.get("uid", ""))
    token = str(data.get("token", ""))
    new_password = str(data.get("new_password", ""))

    try:
        user = User.objects.get(pk=urlsafe_base64_decode(uid).decode())
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return error(RESET_LINK_INVALID)

    if not default_token_generator.check_token(user, token):
        return error(RESET_LINK_INVALID)

    if not new_password:
        return error("Please enter a new password.")

    # Same password rules as sign-up (settings.AUTH_PASSWORD_VALIDATORS)
    try:
        validate_password(new_password, user=user)
    except ValidationError as exc:
        return error(" ".join(exc.messages))

    # set_password hashes the new password. Changing it also makes this link
    # (and any other reset links already sent) stop working.
    user.set_password(new_password)
    user.save()
    return JsonResponse({"message": "Your password has been reset. You can sign in now."})