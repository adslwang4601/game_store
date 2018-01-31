from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
import sys
sys.path.append('..')
from django.http import HttpResponse
from gameinfo.models import Game
from .cart import Cart
from .forms import CartAddProductForm

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Game, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(game=product,
                quantity=cd['quantity'],
                update_quantity=cd['update'])
    # return HttpResponse("Here's the text of the Web page.")
    return redirect('cart_detail')
    # return render(request, 'cart/detail.html', {'cart': cart})


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Game, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')
    # return render(request, 'cart/detail.html', {'cart': cart})


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

