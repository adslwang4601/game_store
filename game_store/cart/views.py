from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
import sys
sys.path.append('..')
from django.http import HttpResponse
from gameinfo.models import Game
from .cart import Cart
from .forms import CartAddGameForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from .models import Order
# from .forms import OrderCreateForm
from .cart import Cart

@login_required
@require_GET
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})



@login_required
@require_POST
def cart_add(request, game_id):
    cart = Cart(request)
    game= get_object_or_404(Game, id=game_id)
    cart.add(game=game)
    cart.save()
    # form = CartAddGameForm(request.POST)
    # if form.is_valid():
    #     cd = form.cleaned_data
    #     cart.add(game=game)
    # return HttpResponse("Here's the text of the Web page.")
    return redirect('cart_detail')
    # return render(request, 'cart/detail.html', {'cart': cart})


@login_required
@require_POST
def cart_remove(request, game_id):
    cart = Cart(request)
    game = get_object_or_404(Game, id=game_id)
    cart.remove(game)
    return redirect('cart_detail')


def order_create(request):
    my_cart = Cart(request)
    if request.method == 'POST':
        game_ids = my_cart.cart.keys()
        gset = Game.objects.filter(id__in= game_ids)
        for game_id, item in zip(my_cart.cart.keys(), my_cart):
            if request.user.user_profile._ownedGames.filter(id__exact=game_id).count() > 0:
                messages.error(request, "You already own the game %s. This item has been removed from the cart" % item['game'])
        # If somehow the cart is empty, deny the order creation and redirect the user to the cart.
        if len(my_cart) < 1:
            messages.warning(request, "The cart is empty!")
            return redirect('detail')
        order = Order.objects.create(_player=request.user.user_profile,
                                     )
        order._games.set(gset.all())
        order.save()
        messages.info(request, "Order created successfully.")
        # Retrieve the ID and redirect the user to the order detailed view.
        return render(request, 'cart/create.html', {'cart':my_cart})






