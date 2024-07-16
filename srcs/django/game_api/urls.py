from django.urls import path
from . import views

# [/game_api/]

urlpatterns = [
    path('', views.who_am_i),
    path('who_am_i/', views.who_am_i),

]
