from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

# Show accounts on the admin site (http://127.0.0.1:8000/admin/) using
# Django's standard user screens.
admin.site.register(User, UserAdmin)
