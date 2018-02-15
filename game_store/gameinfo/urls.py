from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^leader_board/$', views.leader_board, name='leader_board'),
    url(r'^search/$', views.search_game, name="search"),
    url(r'^(?P<category_slug>[-\w]+)/$',
        views.game_list,
        name='game_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.game_detail, name='game_detail'),
    # url(r'^search/$',views.search_game,name="search")
    url(r'^game_leader_board/(?P<game_id>[0-9]+)/$', views.game_leader_board, name='game_leader_board'),
    url(r'', views.game_list, name='game_list'),

]
