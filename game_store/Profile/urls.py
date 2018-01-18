from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.contrib.auth.views import login, logout
from .views import register

urlpatterns = [
    path(u'^login/$', login, {'template_name': 'Profile/login.html'}, name='login'),
    path(u'^logout/$', logout, {'template_name': 'Profile/logout.html'}, name='login'),
    path(u'^register/$', register, {'template_name': 'Profile/register.html'}, name='register')
]
