from django.urls import path
from .views import get_game_state, move_paddle, update_game ,start_game, initialize_game, delete_game
from mysite.view import game_view
from django.urls import include, path
from rest_framework import routers
from .views import *
from ia_op.views import train_ai_view ,test_ai_view


urlpatterns = [
    path('state/', get_game_state, name='get_game_state'),
    path('move/', move_paddle, name='move_paddle'),
    path('update/', update_game, name='update_game'),
    path('start/', start_game, name='start_game'),
    path('auth/', include('rest_framework.urls')),
    path('train_ai/', train_ai_view, name='train_ai'),
    path('test_ai/', test_ai_view, name='test_ai'),
    path('init/', initialize_game, name='initialize_game'), 
    path('init2/',intirelation, name='intirelation'), 
    path('non/', delete_game, name='delete_game'), 
]   