from django.shortcuts import render
from .models import Todo
from django.shortcuts import get_object_or_404

def homepage(request):

    # put all the todos into context so we can see them on the page
    context = { "all_todos": Todo.objects.all() }
    return render(request, 'todo_app/homepage.html', context)

def show_todo(request, pk):
    # found_todo = Todo.objects.get(pk=pk)
    # this will find the item or else throw a 404 screen
    found_todo = get_object_or_404(Todo, pk=pk)
    context = { "todo_item": found_todo }
    return render(request, 'todo_app/show_todo.html', context)