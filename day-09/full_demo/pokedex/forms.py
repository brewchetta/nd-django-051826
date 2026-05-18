from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Pokemon, PokemonType

User = get_user_model()

# AUTH FORMS

# special form using the UserCreationForm for signing up
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

# SEARCH FORMS

class SearchForm(forms.Form):
    name = forms.CharField(max_length=100)

# FAVORITE FORM / BUTTON

class FavoriteForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.HiddenInput)
    pokemon_id = forms.IntegerField(widget=forms.HiddenInput)
    # pokemon_types = forms.ModelMultipleChoiceField(
    #     queryset=PokemonType.objects.all(),
    #     widget=forms.HiddenInput
    # )