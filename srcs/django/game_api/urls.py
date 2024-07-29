from django.urls import path
from .views import get_game_state, move_paddle, update_game
from mysite.view import game_view
from django.urls import include, path
from rest_framework import routers
from .views import *


urlpatterns = [
	path('state/', get_game_state, name='get_game_state'),
	path('move/', move_paddle, name='move_paddle'),
	path('update/', update_game, name='update_game'),
	path('', game_view, name='game_view'),
	path('api-auth/', include('rest_framework.urls'))
]