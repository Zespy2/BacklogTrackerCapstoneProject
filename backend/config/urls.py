from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>CONNECTION TERMINATED BY NETWATCH</h1><p>You have attempted to reach into the Old Net, beyond the Blackwall. Such intrusions are prohibited in order to contain R.A.B.I.D.S and as such, we have terminated your connection. Netwatch agents have been dispatched to your location.</p>")

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
