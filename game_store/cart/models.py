from django.db import models
import sys
sys.path.append('..')
from gameinfo.models import Game
from Profile.models import User_Profile
from django.contrib.auth.models import AnonymousUser, User
from django.utils import timezone


class Order(models.Model):
    # PaymentId
    id = models.AutoField(primary_key=True)

    # One order only has one player, but one player has many order
    # Buyer
    _player = models.ForeignKey(User_Profile, on_delete=models.CASCADE)

    # Items bought
    _games = models.ManyToManyField(Game, default=None, blank=True)

    # When the order was created
    order_time = models.DateTimeField(default=timezone.now, null=False)

    # When the order was paid
    payment_time = models.DateTimeField(default=timezone.now, null=False)

    # Whether be paid
    paid = models.CharField(default=False, max_length=20)

    # Total Price
    total = models.DecimalField(max_digits=6, decimal_places=2, blank=False)

    class Meta:
        ordering = ('-order_time',)

    def __str__(self):
        return 'Order {}'.format(self.id)



# class OrderItem(models.Model):
#     # One OrderItem only has one oder, but one oder has many orderitems
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
#     product = models.ForeignKey(Game, related_name='order_items', on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     quantity = models.PositiveIntegerField(default=1)
#
#     def __str__(self):
#         return '{}'.format(self.id)
#
#     def get_cost(self):
#         return self.price * self.quantity



# Create your models here.
