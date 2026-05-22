from django import forms
from .models import Todo, Tea

class CreateTodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['name']

class EditTodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['name', 'completed']

class TeaForm(forms.ModelForm):
    class Meta:
        model = Tea
        fields = ['name', 'description', 'image_url', 'caffeinated']