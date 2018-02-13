from django.shortcuts import render, get_object_or_404
from .models import Category, Game
import sys
from django.http.response import HttpResponseRedirect, JsonResponse
from django.urls import reverse
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

# def search_game(request):
#     q = request.GET.get('q')
#     if not q:
#         # return render(request, 'game/dashboard.html')
#         return HttpResponseRedirect(reverse('game_list'))

#     # games = [g.to_json() for g in Game.objects.filter(name__icontains=q)]
#     # # user = request.user
#     # # profile = User_Profile.objects.filter(user=user).get()
#     # # games = [g.to_json(request.user) for g in profile._ownedGames.all()]    
#     # # Return a list of games owned by the logged user
#     # context = {"games":games}
#     # return render(request, 'game/search.html',context)
#     games = Game.objects.filter(name__icontains=q)
#     return render(request,'game/search.html',{"games":games})



