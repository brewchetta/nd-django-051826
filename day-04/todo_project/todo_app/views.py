from django.shortcuts import render, redirect, get_object_or_404
from .models import Todo
from .forms import CreateTodoForm, EditTodoForm

def homepage(request):
    context = { "all_todos": Todo.objects.all() }
    return render(request, 'todo_app/homepage.html', context)

def create_todo(request):
    # IF WE ARE GETTING A POST REQUEST... HANDLE IT DIFFERENTLY
    if request.method == "POST":
        # fill a new instance of the form with the POST info
        form = CreateTodoForm(request.POST)
        # check if the form is valid
        if form.is_valid():
            # save the form to the database
            form.save()
            # send user back to the homepage
            return redirect('homepage')
        # if invalid...
        else:
            # render the form with errors on the page
            context = { "form": form }
            return render(request, 'todo_app/create_todo.html', context)

    # FOR GET REQUESTS 
    form = CreateTodoForm()
    context = { "form": form }
    return render(request, 'todo_app/create_todo.html', context)

def edit_todo(request, pk):
    found_todo = get_object_or_404(Todo, pk=pk)

    if request.method == "POST":
        form = EditTodoForm(request.POST, instance=found_todo)
        if form.is_valid():
            form.save()
            return redirect('homepage')
        else:
            context = { "form": form }
            return render(request, 'todo_app/edit_todo.html', context)

    form = EditTodoForm(instance=found_todo)
    context = { "form": form }
    return render(request, 'todo_app/edit_todo.html', context)

def delete_todo(request, pk):
    found_todo = get_object_or_404(Todo, pk=pk)

    if request.method == "POST":
        found_todo.delete()
        return redirect('homepage')

    context = { "found_todo": found_todo }
    return render(request, 'todo_app/delete_todo.html', context)