from django.db import models
from Profile.models import User_Profile
from gameinfo.models import Game
from django.db import models
from django.utils import timezone
# Create your models here.

class Game_Score(models.Model):
    played_game = models.ForeignKey(Game,on_delete=models.CASCADE)
    score = models.FloatField(default=0)
    played_time = models.DateTimeField(default=timezone.now)
    _player = models.ForeignKey(User_Profile,on_delete=models.CASCADE)
    

    def __str__(self):
        return str(self.score)

    def to_json(self):
        json_list = {
            'game': self.played_game.name,
            'score': self.score,
            'played_time': str(self.played_time),
            'player': self._player.user.username
        }

        return json_list

class Saved_Game(models.Model):
    played_game = models.ForeignKey(Game,on_delete=models.CASCADE)
    status = models.TextField()
    saved_time = models.DateTimeField(default=timezone.now)
    settings = models.TextField()
    _player = models.ForeignKey(User_Profile,on_delete=models.CASCADE)
    

    def __str__(self):
        return str(self.status)

