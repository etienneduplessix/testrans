"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from mysite import view 
from django.contrib import admin
from django.urls import path, include


handler404 = 'mysite.view.view_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', view.home),
    path('api/', include('ft_api.urls')), # 42 authentication
    path('game_api/', include('game_api.urls')), # custom api fpr game data
    path('logout/',view.logout),
    path('templates/<str:template_name>/', view.get_template, name='get_template'),
    path('<str:template_name>/', view.load_template, name='get_template'),
]
