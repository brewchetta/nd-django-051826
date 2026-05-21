from django.shortcuts import render
from .models import Todo

def homepage(request):
    context = { "all_todos": Todo.objects.all() }
    return render(request, 'todo_app/homepage.html', context)