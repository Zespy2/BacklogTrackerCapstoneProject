from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Django's built-in admin site: http://127.0.0.1:8000/admin/
    # Lets you browse and edit the accounts database in your browser.
    path("admin/", admin.site.urls),
    # Sign-in / sign-up API used by the React site
    path("api/", include("accounts.urls")),
]
