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
from django.urls import path
from mysite.view import home
from mysite.view import home, api, callback 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', view.api, name='api'),
    path('', view.home, name='home'),
    path('api/callback/', callback, name='callback'), 
    path('item/', view.item_list, name='item_list'),
    path('item/add/', view.add_item, name='add_item'),
    path('templates/<str:template_name>/', view.get_template, name='get_template'),
    path('<str:template_name>/', view.load_template, name='get_template'),
]

