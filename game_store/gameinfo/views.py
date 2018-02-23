from django.shortcuts import render, get_object_or_404
from .models import Category, Game
import sys
from django.http.response import HttpResponseRedirect, JsonResponse
from django.urls import reverse
sys.path.append('..')
from cart.forms import CartAddGameForm
from collections import OrderedDict
from players.models import Game_Score
from django.http.response import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from django.shortcuts import render
from gameinfo.models import Game

def game_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    games = Game.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        games = games.filter(category=category)
    return render(request,
                  'gameinfo/list.html',
                  {'user': request.user,
                  'category': category,
                  'categories': categories,
                  'games': games})

def game_detail(request, id, slug):
    game = get_object_or_404(Game, id=id, slug=slug)
    cart_game_form = CartAddGameForm()
    return render(request, 'gameinfo/detail.html', {'game': game, 'cart_game_form': cart_game_form})

# This view is public: it does not require any authentication
def game_leader_board(request,game_id):
    game = Game.objects.get(id=game_id)

    # game_scores = Game_Score.objects.filter(played_game=game).values('_player__user__username').annotate(score=Max('score'))[0:10]
    game_scores = Game_Score.objects.filter(played_game=game).order_by("-score")
    scores = [s.to_json() for s in game_scores]
    context = {"scores":scores}
    return render(request, 'game/game_leader_board.html', context)


def search_game(request):
    q = request.GET.get('q')
    if not q:
        return HttpResponseRedirect(reverse('game_list'))
    games = Game.objects.filter(name__icontains=q)
    return render(request,'game/search.html',{"games":games})

def leader_board(request,category_slug=None):
    category = None
    categories = Category.objects.all()
    games = Game.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        games = games.filter(category=category)
    return render(request,
                  'game/leader_board.html',
                  {'category': category,
                  'categories': categories,
                  'games': games})







