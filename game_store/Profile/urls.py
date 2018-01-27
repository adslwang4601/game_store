from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
# from django.contrib.auth.views import login, logout, password_change, password_change_done, password_reset, \
#     password_reset_done, password_reset_confirm, password_reset_complete
from django.contrib.auth.views import login, logout, password_change, password_change_done, password_reset, \
    password_reset_done, password_reset_confirm, password_reset_complete
from .views import register, user_login, edit, my_profile
from django.urls import reverse_lazy
from django.contrib.auth import views


urlpatterns = [
    # # url(r'^log_in/$', user_login, {'template_name': 'Profile/log_in.html'}, name='login'),
    # path('log_in/', user_login, name='log_in'),
    # # url(r'^logged_out/$', views.logout, {'template_name': 'registration/logged_out.html'}, name='logged_out'),
    # path('logged_out/', views.LogoutView.as_view(template_name='Profile/logged_out.html'), name='logged_out'),
    # path('register/', register, name='register'),
    #
    # # change password urls
    # path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    # path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    #
    # # restore password urls
    # path('password_reset/', views.PasswordResetView.as_view(html_email_template_name='registration/pass222word_reset_email.html'), name='password_reset'),
    # path('password_reset/done/', views.PasswordResetDoneView.as_view(),  name='password_reset_done'),
    # path(
    #     'password_reset/confirm/(?P<uidb64>[-\w]+)/(?P<token>[-\w]+)/', views.PasswordResetConfirmView.as_view(),
    #     name='password_reset_confirm'
    # ),
    # path('password_reset/complete/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),


    path('log_in/', user_login, name='log_in'),
    path('logout/', views.LogoutView.as_view(template_name='Profile/logged_out.html'), name='logged_out'),
    path('register/', register, name='register'),

    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('my_profile/', my_profile, name='my_profile'),
    path('edit/', edit, name='edit')
]
