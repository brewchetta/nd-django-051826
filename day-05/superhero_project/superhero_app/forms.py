from django import forms
from .models import Superhero, UserProfile

class SuperheroForm(forms.ModelForm):
    class Meta:
        model = Superhero
        fields = ['alias', 'real_name', 'powers', 'origin_story']


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

# getting the user this way is safer and more secure
User = get_user_model()

# UserCreationForm is a special form for making users
class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        # password1 / password2 is a password confirmation pattern

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'favorite_superhero', 'status']