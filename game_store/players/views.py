from django.shortcuts import render
from django.contrib import  messages
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseRedirect, HttpResponse, JsonResponse
from gameinfo.models import Game, Game_Sale
from Profile.models import User, User_Profile
from cart.models import Order
from django.urls import reverse
import datetime
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from .forms import ScoreForm, SaveForm, LoadForm
from django.http.response import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Saved_Game,Game_Score
from gameinfo.models import Game
import json

@login_required(login_url='log_in')
@permission_required(perm='Profile.players')
def owned_games(request):
    games = [g.to_json() for g in request.user.user_profile._ownedGames.all()]
    context = {'user': request.user, "games":games}
    return render(request, 'game/owned_games.html', {'user': request.user, 'games': games})


@login_required(login_url='log_in')
@permission_required(perm='Profile.players')
def play_game(request,game_id):
    # return HttpResponse("play_game")
    game = get_object_or_404(Game, id=game_id)
    whether_owned = request.user.user_profile._ownedGames.filter(id=game_id).exists()
    if not whether_owned:
        messages.error(request, "Sorry, you don't own the game.")
        return HttpResponseRedirect(reverse("game_list"))

    if request.method == 'GET':
        context = {'game': game.to_json(),'game_url': game.url}
        return render(request,"game/play_game.html", context)

    elif request.method == 'POST':
        response = {
            "error": None,
            "result": None
        }
        if request.POST.get('messageType') == 'SCORE':
            scoreForm = ScoreForm(request.POST)
            if scoreForm.is_valid():
                Game_Score.objects.create(played_game=game,
                                      score=scoreForm.cleaned_data['score'],
                                      played_time=timezone.now(),
                                      _player=request.user.user_profile)
            else:
                response['error'] = scoreForm.errors
            return  JsonResponse(response)

        elif  request.POST.get('messageType') == 'SAVE':
            saveForm = SaveForm(request.POST)
            if saveForm.is_valid():
                saved_game = Saved_Game.objects.update_or_create( played_game=game,
                                                                _player=request.user.user_profile)[0]
                saved_game.saved_time = timezone.now()
                saved_game.state = saveForm.cleaned_data['gameState']
                saved_game.save()
            else:
                response['error'] = saveForm.errors

            return JsonResponse(response)

        elif request.POST.get('messageType') == 'LOAD_REQUEST':
            saved_game = Saved_Game.objects.filter( played_game=game,
                                                    _player=request.user.user_profile
                                              ).order_by("-saved_time")
            if saved_game.exists():
                response['result'] = saved_game[0].state
            else:
                response['error'] = "No saved game state."

            return JsonResponse(response)

        else:
            response['error'] = "Invalid message type."
            return JsonResponse(response)
    else:
        return HttpResponse("Invalid request method")


@login_required(login_url='log_in')
@permission_required(perm='Profile.players')
def player_game_score(request, game_id):
        game = Game.objects.get(id=game_id)
        try:
            game_scores = Game_Score.objects.filter(played_game=game,_player=request.user.user_profile).order_by("-score")
        except ObjectDoesNotExist:
            return HttpResponse("No game score available")
        scores = [s.to_json() for s in game_scores]
        context = {'user': request.user, "scores":scores}
        
        return render(request, 'game/scores.html', context)





