from django.shortcuts import render

from ..gameinfo.models import Game

# Create your views here.
def uploads(request,user_id)
    """Game uploads"""
    games_published = Games.objects.filter(publisher=user_id)
    context = {
    'games' : games_published
    }
    return render(request, 'game_store',uploads.html', context)
