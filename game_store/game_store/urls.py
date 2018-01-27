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
<<<<<<< HEAD
# import sys
# sys.path.insert(0, '/Users/adslwang4601/Desktop/course/game_store/game_store/Store')
# from views import dashboard
=======
from Profile import views

import sys
sys.path.append("..")
>>>>>>> 68a950c39ce0baf3536ced2bf2823cf50b7a8961

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Store.urls')),
<<<<<<< HEAD
    path('profile/', include('Profile.urls')),
=======
    path('Profile/', include('Profile.urls')),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    views.activate, name='activate'),
    path('developers/', include('developers.urls')),
    path('', include('players.urls')),
>>>>>>> 68a950c39ce0baf3536ced2bf2823cf50b7a8961
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
<<<<<<< HEAD
                        document_root=settings.MEDIA_ROOT)
=======
                        document_root=settings.MEDIA_ROOT)
>>>>>>> 68a950c39ce0baf3536ced2bf2823cf50b7a8961
