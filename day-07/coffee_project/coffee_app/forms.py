from django import forms
from .models import Beverage

class BeverageForm(forms.ModelForm):
    class Meta:
        model = Beverage
        fields = ['name', 'caffeinated']