from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class User_Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_profile')
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True, null=True)
    city = models.CharField(max_length=100, default='', blank=True)
    country = models.CharField(max_length=100, default='', blank=True)
    _ownedGames = models.ManyToManyField('gameinfo.Game', default=None, blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)



