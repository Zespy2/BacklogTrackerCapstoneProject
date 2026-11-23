from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse

def home(request):
    return HttpResponse("If you're seeing this, the backend's up. Move along. Go. leave. Seriously, go. NIGHTMARENIGHTMARENIGHTMARENIGHTMARENIGHTMARE")

urlpatterns = [
    # Django's built-in admin site: http://127.0.0.1:8000/admin/
    # Lets you browse and edit the accounts database in your browser.
    path("admin/", admin.site.urls),
    # Sign-in / sign-up API used by the React site
    path("api/", include("accounts.urls")),
    path('', home, name='home'),
    path(
        "api/recommendations/",
        include("recommendations.urls"),
    ),
]
