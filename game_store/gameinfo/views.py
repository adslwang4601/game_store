from django.shortcuts import render, get_object_or_404
from .models import Category, Game
import sys
sys.path.append('..')
from cart.forms import CartAddGameForm

def game_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    games = Game.objects.all()
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        games = games.filter(category=category)
    return render(request,
                  'gameinfo/list.html',
                  {'category': category,
                  'categories': categories,
                  'games': games})

def game_detail(request, id, slug):
    game = get_object_or_404(Game, id=id, slug=slug)
    cart_game_form = CartAddGameForm()
    return render(request, 'gameinfo/detail.html', {'game': game, 'cart_game_form': cart_game_form})



