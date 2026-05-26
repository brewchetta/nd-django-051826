from django import forms
from .models import Superhero

class SuperheroForm(forms.ModelForm):
    class Meta:
        model = Superhero
        fields = ['alias', 'real_name', 'powers', 'origin_story']