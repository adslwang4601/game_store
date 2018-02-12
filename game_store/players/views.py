from django.shortcuts import render
from django.contrib import  messages
from django.shortcuts import get_object_or_404
from gameinfo.models import Game, Game_Sale, Game_Score
from Profile.models import User, User_Profile
from cart.models import Order

def owned_games(request):
    games = [g.to_json(request.user) for g in request.user.user_profile._ownedGames.all()]
    # user = request.user
    # profile = User_Profile.objects.filter(user=user).get()
    # games = [g.to_json(request.user) for g in profile._ownedGames.all()]    
    # Return a list of games owned by the logged user
    context = {'user': request.user, "games":games}
    return render(request, 'game/owned_games.html', {'user': request.user, 'games': games})