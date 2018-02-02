from decimal import Decimal
from django.conf import settings
from gameinfo.models import Game

class Cart(object):
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, game):
        """
        Add a product to the cart or update its quantity.
        """
        game_id = str(game.id)
        if game_id not in self.cart:
            self.cart[game_id] = {'price': str(game.price)}
        self.save()

    def save(self):
        # update the session cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # mark the session as "modified" to make sure it is saved
        self.session.modified = True

    def remove(self, game):
        """
        Remove a product from the cart.
        """
        game_id = str(game.id)
        if game_id in self.cart:
            del self.cart[game_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        game_ids = self.cart.keys()
        # get the product objects and add them to the cart
        games = Game.objects.filter(id__in=game_ids)
        for game in games:
            self.cart[str(game.id)]['game'] = game

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            yield item

    def __len__(self):
        """
        Count all items in the cart.
        """
        return len(self.cart.keys())
        # return sum(item['game'] for item in self.cart)

    def get_total_price(self):
        return sum(Decimal(item['price']) for item in self.cart.values())

    def clear(self):
        # remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True




