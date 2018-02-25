from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.contrib.auth.views import login, logout, password_change, password_change_done, password_reset, \
    password_reset_done, password_reset_confirm, password_reset_complete
from .views import register, user_login, edit, my_profile, activate
from django.urls import reverse_lazy
from django.contrib.auth import views
from django.views.generic import TemplateView
# app_name = 'profile'
urlpatterns = [


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
    path('edit/', edit, name='edit'),

    path('confirm_email/', TemplateView.as_view(template_name="Profile/acc_active_email.html"), name='confirm_email' ),
    path('activate/(<uidb64>/<token>/', activate, name='activate')
]
