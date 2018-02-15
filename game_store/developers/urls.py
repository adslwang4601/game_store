from django.conf.urls import include, url
from .views import developer_games, edit_game, request_developer_statistics

urlpatterns = [
    # For Logged users=>Developers
    url(r'^games/$', developer_games, name='dev_games'),
    url(r'^edit_game/(?P<game_id>[0-9]+)/$', edit_game, name='edit_game'),
    url(r"^stats/$", request_developer_statistics, name='statistics'),
    # url(r'^inventory/$', views.inventory, name='inventory'),
]
