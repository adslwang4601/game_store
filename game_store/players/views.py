from django.shortcuts import render
from django.contrib import  messages
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponseRedirect, HttpResponse, JsonResponse
from gameinfo.models import Game, Game_Sale
from Profile.models import User, User_Profile
from cart.models import Order
from django.urls import reverse
import datetime
from .forms import MessageForm,MessageScoreForm, MessageSaveForm, MessageLoadForm
from django.http.response import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import Saved_Game,Game_Score
from gameinfo.models import Game
import json

def owned_games(request):
    games = [g.to_json() for g in request.user.user_profile._ownedGames.all()]
    context = {'user': request.user, "games":games}
    return render(request, 'game/owned_games.html', {'user': request.user, 'games': games})

def play_game(request,game_id):
    # return HttpResponse("play_game")
    game = get_object_or_404(Game, id=game_id)
    wheter_owned = request.user.user_profile._ownedGames.filter(id=game_id).exists()
    if not wheter_owned:
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
        # Parse the message type and basic sanitizing
        form = MessageForm(request.POST)
        if not form.is_valid():
            response['error'] = form.errors
            return JsonResponse(status=400, data=response)

        # Parse the specific message and handle it.
        if form.cleaned_data['messageType'] == 'SCORE':
            # The player has finished a match and there is a score notification.
            # let's save it on the db.
            scoreForm = MessageScoreForm(request.POST)
            if not scoreForm.is_valid():
                response['error'] = scoreForm.errors
                return JsonResponse(status=400, data=response)

            Game_Score.objects.create(played_game=game,
                                         score=scoreForm.cleaned_data['score'],
                                         played_time=datetime.datetime.utcnow(),
                                        _player=request.user.user_profile,
                                       )

            return JsonResponse(status=201, data=response)

        elif form.cleaned_data['messageType'] == 'SAVE':
            # The player wants to save the current game status
            # let's save it on the db.
            saveForm = MessageSaveForm(request.POST)
            if not saveForm.is_valid():
                response['error'] = saveForm.errors
                return JsonResponse(status=400, data=response)

            saving = Saved_Game.objects.update_or_create( played_game=game,
                                                         _player=request.user.profile)[0]
            saving.savedDate = datetime.datetime.utcnow()
            saving.status = saveForm.cleaned_data['gameState']
            # settings??
            saving.save()
            return JsonResponse(status=201, data=response)

        elif form.cleaned_data['messageType']=='LOAD_REQUEST':
            loadForm = MessageLoadForm(request.POST)
            if not loadForm.is_valid():
                response['error'] = loadForm.errors
                return JsonResponse(status=400, data=response)

            saving = Saved_Game.objects.filter( played_game=game,
                                                _player=request.user.user_profile
                                              ).order_by("-saved_time")

            if saving.exists():
                response['result'] = saving[0].status
                return JsonResponse(status=200, data=response)
            else:
                response['result'] = None
                response['error'] = "There are no saved games."
                return JsonResponse(status=200, data=response)

        else:
            response['error'] = "Invalid message type."
            return JsonResponse(status=400, data=response)

    else:
        return HttpResponse(status=405, content="Invalid method specified.")

def player_game_score(request, game_id):
        game = Game.objects.get(id=game_id)
        try:
            game_scores = Game_Score.objects.filter(played_game=game,_player=request.user.user_profile).order_by("-score")
        except ObjectDoesNotExist:
            return HttpResponse("Game_Score id does not exist.")
        scores = [s.to_json(request.user) for s in game_scores]
        context = {'user': request.user, "scores":scores}
        
        return render(request, 'game/scores.html', context)





