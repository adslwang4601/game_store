from django.forms import ModelForm
from ..gameinfo.models import Game

class Developer_GameForm(ModelForm):

    class Meta
    models = Game
    fields = ['url', 'price', 'title', 'category', 'icons', 'image','published_date' ]

    def save(self, commit=True)
        game = super(Developer_GameForm,self).save(commit=False)

        if commit:
            game.save()
        return game    
