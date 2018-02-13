# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.db.models import Q
from django.http.response import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from gameinfo.models import Game
def dashboard(request):
    # backend = request.session['_auth_user_backend']
    return render(request, 'game/dashboard.html')


def search_game(request):
    q = request.GET.get('q')
    if not q:
        # return render(request, 'game/dashboard.html')
        return HttpResponseRedirect(reverse('game_list'))

    # games = [g.to_json() for g in Game.objects.filter(name__icontains=q)]
    # # user = request.user
    # # profile = User_Profile.objects.filter(user=user).get()
    # # games = [g.to_json(request.user) for g in profile._ownedGames.all()]    
    # # Return a list of games owned by the logged user
    # context = {"games":games}
    # return render(request, 'game/search.html',context)
    games = Game.objects.filter(name__icontains=q)
    return render(request,'game/search.html',{"games":games})

