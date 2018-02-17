import sys
sys.path.append("..")
from django.shortcuts import render, get_object_or_404
from django.http.response import HttpResponseRedirect, JsonResponse, HttpResponse
from gameinfo.models import Game
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from .forms import Developer_GameForm
from django.contrib import messages
from django.urls import reverse
import json
import datetime
from cart.models import Order
from django.db import connection
from django.db.models import Sum, Count


@login_required(login_url='log_in')
@permission_required(perm='Profile.developer')
def developer_games(request):
    # List all the games published by the developer and provide a form for adding a new one
    if request.method == 'GET':
        # Retrieve all the games of the current developer
        dev_games = Game.objects.filter(publisher=request.user.user_profile)

        response = {}
        games = []
        response['games'] = games
        for g in dev_games:
            tmp = g.to_json()
            response['games'].append(tmp)

        # If the request is via Ajax, return json data representation
        if request.is_ajax():
            return JsonResponse(data=response)

        else:
            # Create a new form to be used in the template
            form = Developer_GameForm()
            return render(request, 'developers/developed_games.html', {'form': form, 'user': request.user, 'games': games})
    elif request.method == 'POST':
        # Let's check if the form we got is OK. If there is something wrong, just return it to the view.
        # Otherwise proceed.
        form = Developer_GameForm(request.POST)
        if not form.is_valid():
            return HttpResponse(status=405, content="Invalid method.")
            # return render(request, "registration/register.html", {'form': form})
        else:
            # Regardless of the user's choice, update the publisher of this game.
            form.instance.publisher = request.user.user_profile
            form.save()
            # Retrieve all the games of the current developer
            dev_games = Game.objects.filter(publisher=request.user.user_profile)
            games = [x.to_json() for x in dev_games]

            messages.success(request=request, message='The game has been added successfully!')
            return render(request, 'developers/developed_games.html', {'form': Developer_GameForm, 'user': request.user, 'games':games})
    else:
        return HttpResponse(status=405, content="Invalid method.")


@login_required(login_url='log_in')
@permission_required(perm='Profile.developer')
def edit_game(request, game_id):
    if request.method == 'GET':

        # Retrieve the data from the db, starting from the game_id and use it to pre-populate the form
        # If the game does not belong to him, we send a 404 instead of a 401 error.
        game = get_object_or_404(Game, id=game_id, publisher=request.user.user_profile)
        form = Developer_GameForm(instance=game)
        return render(request, 'developers/edit_game.html', {'form': form, 'user': request.user})

    elif request.method == 'POST':
        # Retrieve the data from the db, starting from the game_id and use it to pre-populate the form
        # If the game does not belong to him, we send a 404 instead of a 401 error.
        game = get_object_or_404(Game, id=game_id, publisher=request.user.user_profile)
        form =Developer_GameForm(request.POST, instance=game)

        if not form.is_valid():
            messages.error(request, "Please check the form errors and try egain.")
            return render(request, 'developers/edit_game.html', {'form': form, 'user': request.user})
        else:
            if ('action' not in request.POST) or (request.POST['action'].lower() not in ['delete', 'save']):
                messages.error(request=request, message='Missing or invalid action parameter.')
                return HttpResponseRedirect(redirect_to=reverse('dev_games'))

            # Ok, perform the requested operation
            if request.POST['action'].lower() == 'save':
                game = form.save()
                messages.success(request=request, message='Game updated successfully.')
                return HttpResponseRedirect(redirect_to=reverse('dev_games'))
            elif request.POST['action'].lower() == 'delete':
                game.delete()
                messages.success(request=request, message='Game removed successfully.')
                return HttpResponseRedirect(redirect_to=reverse('dev_games'))
            else:
                messages.error(request=request, message='Missing or invalid action parameter.')
                return render(request, 'developers/developed_games.html', {'form': form, 'user': request.user})

    else:
        return HttpResponse(status=405, content="Invalid method.")


@login_required(login_url='log_in')
@permission_required(perm='Profile.developer')
def request_developer_statistics(request):

    year = request.GET.get('year')

    if year is None:
        year = str(datetime.datetime.now().year)

    stats_by_game = get_transactions_by_game(request.user.user_profile, year = year)
    stats_history = get_transaction_history(request.user.user_profile, year=year)

    context = {}

    context["stats_by_game"] = stats_by_game
    context["stats_history"] = stats_history
    context["year"] = year
    context["last_year"] = int(year) - 1
    context["next_year"] = int(year) + 1

    return render(request, "developers/dev_stats.html", context)

def get_transactions_by_game(user, year=None, reverse=True):
    games = Game.objects.filter(publisher=user)

    bought_counts = []

    # games_data = Order.objects.filter(games_id_in=games,
    #                                   status='yes',
    #                                         )
    game_list = []
    for game in games:
        # game_list.append(game)
        # transactions = game.objects.filter()
        # number_of_transactions = transactions.count()
        # revenue = game.price * number_of_transactions

        transactions = Order.objects.filter(_games__id=game.id, paid='yes')
        # print(len())
        number_of_transactions = transactions.count()
        revenue = game.price * number_of_transactions
        # revenue = transactions.aggregate(Sum('total'))['total__sum']
    # Group_by _games
    # data = games_data.values("_games").annotate(Count('id'))
    # for d in data:
    #     game_name = Game.objects.get(id=d['_games']).name
    #     pie.append({'label': game_name, 'value': d['id__count']})

        # transactions = game.transactions
        # transactions = 0


        # data = transactions.values('_games').annotate(Count('id'))

        games_stats = {"game": game, "copies_sold": number_of_transactions, 'revenue': revenue}

        bought_counts.append(games_stats)

    return sorted(bought_counts, key=lambda k: k['revenue'], reverse=reverse)

def get_transaction_history(user, year=None):
    # 1. 提取游戏中包含某个作者的订单
    # 2. 提取该作者的所有游戏
    # 3. 提取包含在某个订单中的所有游戏
    # 4. 创建字典，Key为时间
    buy_history = []
    # transactions = Order.objects.filter(_games__publisher=user)
    games = Game.objects.filter(publisher=user)
    for transaction in Order.objects.all():
        trans_games_names = [trans_game.name for trans_game in transaction._games.all()]
        for game in games:
            if game.name in trans_games_names:
                buy_history.append([transaction.payment_time, game.name, game.price, transaction._player.user.username])

    # total_amount = 0
    # games = Game.objects.filter(publisher=user)
    # if len(games) <= 1:
    #     games = list(games)
    # for game in games:
    #     if year:
    #         transactions = Order.objects.filter(_games__id=game.id, paid='yes', payment_time=year)
    #     else:
    #         transactions = Order.objects.filter(_games__id=game.id, paid='yes')
    #     number_of_transactions = transactions.count()
    #     revenue = game.price * number_of_transactions
    # total_amount += revenue
    # transactions = Order.objects.filter(_games__in=games,
    #                                     paid='yes',
    #                                     )
    # if year:
    #     transactions = transactions.filter(payment_time__year=year)
    #
    # truncate_date = connection.ops.date_trunc_sql('month', 'payment_time')
    # qs = transactions.extra({'month': truncate_date})
    # report = qs.values('month').annotate(copies_sold=Count('pk'), revenue=Sum('total')).order_by('month')

    return buy_history

