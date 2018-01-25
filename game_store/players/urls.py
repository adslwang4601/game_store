from django.urls import path
from . import views

urlpatterns = [
    path('own_games/', views.own_games,name="own_games"),
]