from django.shortcuts import render, get_object_or_404
from .models import Category, Game
import sys
sys.path.append('..')
from cart.forms import CartAddProductForm

def product_list(request, category_slug=None):
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
                  'products': games})

def product_detail(request, id, slug):
    game = get_object_or_404(Game,
                                id=id,
                                slug=slug)
    cart_product_form = CartAddProductForm()
    return render(request,
                  'gameinfo/detail.html',
                  {'product': game,
                   'cart_product_form': cart_product_form})



