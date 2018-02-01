from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
import sys
sys.path.append('..')
from django.http import HttpResponse
from gameinfo.models import Game
from .cart import Cart
from .forms import CartAddProductForm
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
def cart_add(request, product_id):
    # if not request.is_ajax():
    #     messages.error(request, "This view can be only accessed through ajax calls.")
    #     return redirect("cart_detail'")
    #
    # jsondata = {'error': None}
    #
    # # if player has own this game, return error
    # owned_games = request.user.profile._ownedGames.filter(id__exact=product_id)
    # if owned_games.count() > 0:
    #     jsondata['error'] = "You already own this game"
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


@login_required
@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Game, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')
    # return render(request, 'cart/detail.html', {'cart': cart})


# @login_required
# def order_create(request):
#     cart = Cart(request)
#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             order = form.save()
#             for item in cart:
#                 OrderItem.objects.create(order=order,
#                     product=item['product'],
#                     price=item['price'],
#                     quantity=item['quantity'])
#         cart.clear()
#         return render(request,
#                       'cart/created.html',
#                       {'order': order})
#     else:
#         form = OrderCreateForm()
#
#     return render(request,
#             'cart/create.html',
#             {'cart': cart, 'form': form})

def order_create(request):
    my_cart = Cart(request)
    if request.method == 'POST':
        game_ids = my_cart.cart.keys()
        gset = Game.objects.filter(id__in= game_ids)
        for game_id, item in my_cart:
            if request.user.user_profile._ownedGames.filter(id__exact=game_id).count() > 0:
                messages.error(request, "You already own the game %s. This item has been removed from the cart"
                               % item['product'])
        # If somehow the cart is empty, deny the order creation and redirect the user to the cart.
        if len(my_cart) < 1:
            messages.warning(request, "The cart is empty!")
            return redirect('detail')
        order = Order.objects.create(_player=request.user.user_profile,
                                     # _games=gset.set(),
                                     )
        order._games.set(gset.all())
        order.save()
        messages.info(request, "Order created successfully.")
        # Retrieve the ID and redirect the user to the order detailed view.
        return render(request, 'cart/create.html', {'cart':my_cart})






