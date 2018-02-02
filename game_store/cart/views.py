from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
import sys
sys.path.append('..')
from django.http import HttpResponse, HttpResponseNotAllowed
from gameinfo.models import Game
from .cart import Cart
from .forms import CartAddGameForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from .models import Order
# from .forms import OrderCreateForm
from .cart import Cart
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from hashlib import md5
import datetime
from django.conf import settings
from decimal import Decimal


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
def cart_remove(request, game_id):
    cart = Cart(request)
    game = get_object_or_404(Game, id=game_id)
    cart.remove(game)
    return redirect('cart_detail')


def order_create(request):
    total = Decimal(0)
    my_cart = Cart(request)
    if request.method == 'POST':
        game_ids = my_cart.cart.keys()
        gset = Game.objects.filter(id__in= game_ids)
        for game_id, item in zip(my_cart.cart.keys(), my_cart):
            if request.user.user_profile._ownedGames.filter(id__exact=game_id).count() > 0:
                messages.error(request, "You already own the game %s. This item has been removed from the cart" % item['game'])
            else:
                total += item['price']
        # If somehow the cart is empty, deny the order creation and redirect the user to the cart.
        if len(my_cart) < 1:
            messages.warning(request, "The cart is empty!")
            return redirect('cart_detail')
        order = Order.objects.create(_player=request.user.user_profile,
                                     total=total,
                                     paid='no'
                                     )
        order._games.set(gset.all())
        order.save()
        messages.info(request, "Order created successfully.")
        return HttpResponseRedirect(reverse("order_details", kwargs={'order_id': order.id}))
        # Retrieve the ID and redirect the user to the order detailed view.




def order_details(request, order_id):
    if request.method == 'GET':
        my_cart = Cart(request)
        if order_id is None:
            messages.error(request, "Invalid or missing Pid specified.")
            return HttpResponseRedirect(reverse('cart_detail'))

        pid = order_id

        order = None
        try:
            order = Order.objects.get(id=pid)
        except ObjectDoesNotExist:
            messages.error(request, "Invalid or missing Pid specified.")
            return HttpResponseRedirect(reverse('cart_detail'))

        # Is the user in charge of it?
        if order._player != request.user.user_profile:
            messages.error(request, "You are not allowed to manage this order")
            return HttpResponseRedirect(reverse('cart_detail'))

        action = "http://payments.webcourse.niksula.hut.fi/pay/"
        sid = 'webpayment'

        amount = order.total
        success_url = request.build_absolute_uri(reverse("payment_result"))
        cancel_url = request.build_absolute_uri(reverse("payment_result"))
        error_url = request.build_absolute_uri(reverse("payment_result"))
        secret_key = 'e10a4b4a836d62099862b38660f21fa0'

        checksumstr = "pid={}&sid={}&amount={}&token={}".format(pid, sid, amount, secret_key)
        m = md5(checksumstr.encode("ascii"))
        checksum = m.hexdigest()

        return render(request, 'cart/create.html', {'user': request.user,
                                                    'cart': my_cart,
                                                    'action': action,
                                                    'pid': pid,
                                                    'sid': sid,
                                                    'amount': amount,
                                                    'success_url': success_url,
                                                    'cancel_url': cancel_url,
                                                    'error_url': error_url,
                                                    'checksum': checksum})


    else:
        return HttpResponse(content='POST method is prohibited', status=405)


def payment_result(request):

    if request.method == 'GET':
        # Check the payment data is correct
        pid = request.GET['pid']
        ref = request.GET['ref']
        result = request.GET['result']
        checksum = request.GET['checksum']

        # First check: authenticate the request
        sid = "web_payment"  # Fixme Todo: parametrize
        secret_key = "e10a4b4a836d62099862b38660f21fa0"  # Fixme Todo: parametrize

        checksumstr = "pid={}&ref={}&result={}&token={}".format(pid, ref, result,
                                                                secret_key)  # Fixme Todo: parametrize, secret key!
        m = md5(checksumstr.encode("ascii"))
        checksum2 = m.hexdigest()

        if checksum != checksum2:
            messages.error(request, "Invalid checksum. Your payment is invalid.")
            return HttpResponseRedirect(redirect_to=reverse("cart_detail"))

        # Second: verify PID exists
        try:
            order = Order.objects.get(id=pid)
        except ObjectDoesNotExist:
            messages.error(request, "Invalid OrderId specified. Your payment is invalid.")
            return HttpResponseRedirect(redirect_to=reverse("cart_detail"))


        # Third: verify whether user has been changed
        if order._player != request.user.user_profile:
            messages.error(request, 'This order is not created by you and this order is cancel')
            return HttpResponseRedirect(redirect_to=reverse("cart_detail"))

        # Fourth: Check the status
        if order.paid == 'yes':
            messages.error(request, 'The status of the order has been changed, invalid payment')
            return HttpResponseRedirect(redirect_to=reverse("cart_detail"))

        if result == 'success':
            for game in order._games.all():
                order._player._ownedGames.add(game)
            order._player.save()
            order.created = datetime.datetime.now()
            order.paymentRef = ref
            order.paid = 'yes'
            order.save()

            request.session[settings.CART_SESSION_ID] = {}
            return HttpResponseRedirect(redirect_to=reverse('payment_success'))
        elif result == 'cancel':
            order.delete()
            messages.info(request, "The order has been canceled as requested.")
            return HttpResponseRedirect(redirect_to=reverse("cart_detail"))

        elif result == "error":
            order.paid = "error"
            messages.error(request, "There was an error processing the payment. Please try again!")
            return HttpResponseRedirect(redirect_to=reverse('cart_detail'))

    else:
        # This view only supports GET
        return HttpResponse(status=405, content="Invalid method.")


def payment_success(request):
    return HttpResponseRedirect(reverse('game_list'))





