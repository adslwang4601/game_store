"""game_store URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from Profile import views
from django.views.generic import TemplateView


import sys
sys.path.append("..")



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="game/dashboard.html"), name='dashboard'),
    path('cart/', include('cart.urls'), name='cart'),
    path('Profile/', include('Profile.urls'), name='profile'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    path('developers/', include('developers.urls'), name='developers'),
    path('players/', include('players.urls'), name='players'),
    path('accounts/', include('allauth.urls'), name='accounts'),
    path('game/', include('gameinfo.urls'), name='gameinfo')

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                        document_root=settings.MEDIA_ROOT)
