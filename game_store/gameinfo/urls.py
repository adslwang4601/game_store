from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.game_list, name='game_list'),
    url(r'^(?P<category_slug>[-\w]+)/$',
        views.game_list,
        name='game_list_by_category'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',
        views.game_detail,
        name='game_detail'),
]
