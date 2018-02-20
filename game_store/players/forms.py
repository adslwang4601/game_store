from django import forms
from gameinfo.models import Game
from django.core.exceptions import ValidationError
import json

class ScoreForm(forms.Form):
    messageType = forms.CharField(required=True)
    score = forms.FloatField(required=True, widget=forms.HiddenInput())


class SaveForm(forms.Form):
    messageType = forms.CharField(required=True)
    gameState = forms.CharField(required=True, widget=forms.HiddenInput())

    def clean_gameState(self):
        # Check if the game state is serializable by json
        try:
            # Check for validity
            json_test = json.loads(self.cleaned_data['gameState'])
        except ValueError:
            raise ValidationError("The game state is not valid json!")

        return self.cleaned_data['gameState']

# Implementing the following class just for consistency. It is not necessary, but I prefer to keep the code linear and
# consistent
class LoadForm(forms.Form):
    messageType = forms.CharField(required=True)