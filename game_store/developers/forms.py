import sys
sys.path.append('..')
from django.forms import ModelForm
from gameinfo.models import Game, Category
from django import forms
from django.core.exceptions import ValidationError


class Developer_GameForm(ModelForm):
    # Need to check max_length of name, otherwise the django model will truncate the name
    name = forms.CharField(required=True, max_length=80)
    description = forms.CharField(required=True, widget=forms.Textarea())
    # We redefine price so we can define the maximum number of decimals
    price = forms.DecimalField(required=True, decimal_places=2, max_digits=9)
    # slug = forms.ChoiceField(choices=[('action', 'action'), ('puzzle', 'puzzle'),
    #                                   ('adventure', 'adventure'), ('strategy', 'strategy')])
    # Populate at runtime
    category = forms.ModelChoiceField(required=True, queryset=None)

    class Meta:
        model = Game
        fields = ['url', 'slug', 'price', 'name', 'description', 'category', 'icon', 'image', 'published_date']

    def __init__(self, *args, **kwargs):
        super(Developer_GameForm, self).__init__(*args, **kwargs)
        # Dynamically populate the category set
        self.fields['category'].queryset = Category.objects.all()

    def clean_price(self):
        if float(self.cleaned_data['price']) < 0:
            raise ValidationError("Price must be positive.")
        return self.cleaned_data['price']



    # def save(self, commit=True)
    #     game = super(Developer_GameForm,self).save(commit=False)
    #
    #     if commit:
    #         game.save()
    #     return game

