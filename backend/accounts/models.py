from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    One row in the accounts table = one player account.

    AbstractUser already gives us: username, password (stored hashed, never
    as plain text), first_name, last_name, is_staff, is_active, date_joined
    and last_login. We only change email so that it is required and no two
    accounts can share one, because people sign in with their email.

    Add more account fields here later (avatar, bio, favourite platform...),
    then run `python manage.py makemigrations` and `python manage.py migrate`.
    """

    email = models.EmailField("email address", unique=True)

    def __str__(self):
        return self.username
