from django.shortcuts import render, redirect
from .models import Todo
from .forms import TodoForm

def homepage(request):
    context = { "all_todos": Todo.objects.all() }
    return render(request, 'todo_app/homepage.html', context)

def create_todo(request):
    # IF WE ARE GETTING A POST REQUEST... HANDLE IT DIFFERENTLY
    if request.method == "POST":
        # fill a new instance of the form with the POST info
        form = TodoForm(request.POST)
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
            return render(request, 'todo_app/create_todo/html', context)

    # FOR GET REQUESTS 
    form = TodoForm()
    context = { "form": form }
    return render(request, 'todo_app/create_todo.html', context)