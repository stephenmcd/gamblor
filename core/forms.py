
from django import forms


class GameForm(forms.Form):

    amount = forms.IntegerField()
