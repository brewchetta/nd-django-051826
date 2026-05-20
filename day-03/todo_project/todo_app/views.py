from django.shortcuts import render
from .models import Todo, Author
from django.shortcuts import get_object_or_404

def homepage(request):
    # these are the possible query parameters
    # ?completed=true
    # ?name=yoga
    completed = request.GET.get('completed')
    name = request.GET.get('name')

    # get all todo items
    all_todos = Todo.objects.all()

    # if we have the complete=true query parameter
    # filter to only get the todos which have been completed
    if completed == "true":
        all_todos = all_todos.filter(completed=True)

    if completed == "false":
        all_todos = all_todos.filter(completed=False)

    if name:
        all_todos = all_todos.filter(task_name__icontains=name)

    # put all the todos into context so we can see them on the page
    context = { "all_todos": all_todos }
    return render(request, 'todo_app/homepage.html', context)

def show_todo(request, pk):
    # found_todo = Todo.objects.get(pk=pk)
    # this will find the item or else throw a 404 screen
    found_todo = get_object_or_404(Todo, pk=pk)
    context = { "todo_item": found_todo }
    return render(request, 'todo_app/show_todo.html', context)

def authors(request):
    context = { "authors": Author.objects.all() }
    return render(request, 'todo_app/authors.html', context)