from django.urls import path
from . import views

urlpatterns = [
	path('', views.api, name='api'), #default api
	path('callback/', views.callback, name='callback'), #callback

]
