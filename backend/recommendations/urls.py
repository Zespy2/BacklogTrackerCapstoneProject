
from django.urls import path

from .views import game_recommendation

urlpatterns = [
    path("", game_recommendation, name="game_recommendation"),
]
