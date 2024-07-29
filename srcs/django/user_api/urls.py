from django.urls import path
from . import views

urlpatterns = [
	path('', views.who_am_i),
	path('register/', views.register),
	path('login/', views.login),
	path('who_am_i/', views.who_am_i),
	path('online/', views.online),

]
