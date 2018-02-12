from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from .views import owned_games

urlpatterns = [
    path('owned_games/',owned_games,name='owned_games'),
]
