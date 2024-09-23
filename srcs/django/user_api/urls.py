from django.urls import path
from . import views


urlpatterns = [
	path('register/', views.register_view),
	path('profile/<int:id>', views.profile, name='profile'),
	path('change_pass/<int:id>', views.change_pass),
	path('friends/', views.get_friends),
	path('get_profile_data/', views.get_profile_data),
	path('', views.who_am_i),
	path('login/', views.login_view),
	path('who_am_i/', views.who_am_i),
	path('who_is/<str:username>/', views.who_is),
	path('online/', views.online),
]
