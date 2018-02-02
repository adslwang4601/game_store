from django.conf.urls import url
from django.urls import path, re_path
from . import views

urlpatterns = [
    url(r'^$', views.cart_detail, name='cart_detail'),
    # re_path('add/(?P<game_id>d+)/', views.cart_add,
    #         name='cart_add'),
    # re_path('remove/(?P<game_id>d+)/', views.cart_remove,
    #         name='cart_remove'),
    url(r'^add/(?P<game_id>\d+)/$', views.cart_add, name='cart_add'),
    url(r'^remove/(?P<game_id>\d+)/$', views.cart_remove, name='cart_remove'),
    url(r'^create/$', views.order_create, name='order_create'),
    url(r'^order_details/(?P<order_id>[a-zA-Z0-9]+)/$', views.order_details, name='order_details'),
    url(r'^payment_result/$', views.payment_result, name='payment_result'),
    url(r'^payment_success/$', views.payment_success, name='payment_success'),

]

