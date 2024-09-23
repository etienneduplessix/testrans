from django.urls import path
from .views import get_game_state, move_paddle, update_game ,create_game
from mysite.view import game_view
from django.urls import include, path
from rest_framework import routers
from .views import *


urlpatterns = [
    path('game_api/', include('game_api.urls')),
]
