<<<<<<< HEAD
from django.urls import path
from . import views

urlpatterns = [
    path('own_games/', views.own_games,name="own_games"),
]
=======
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
# import sys
# sys.path.insert(0, '/Users/adslwang4601/Desktop/course/game_store/game_store/Store')
# from views import dashboard

urlpatterns = [
    path('admin/', admin.site.urls),

]
>>>>>>> da454813627acbd30e664fe087b02192f9f13adb