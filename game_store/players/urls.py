from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from .views import owned_games,play_game,player_game_score

urlpatterns = [
    path('owned_games/',owned_games,name='owned_games'),
    url(r'^play/(?P<game_id>[0-9]+)/$', play_game, name='play_game'),
    url(r'^scores/(?P<game_id>[0-9]+)/$', player_game_score, name='scores'),

]
