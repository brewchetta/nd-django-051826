from django.shortcuts import render
from .models import Superhero

# HOME #
def home(request):
    return render(request, 'superhero_app/home.html')

# SUPERHERO INDEX #
def superhero_index(request):
    context = { 'superheroes': Superhero.objects.all() }
    return render(request, 'superhero_app/superhero_index.html', context)

from .forms import SuperheroForm
from django.shortcuts import redirect

# SUPERHERO CREATE #
def superhero_create(request):
    # POST #
    if request.method == "POST":
        form = SuperheroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('superhero_index')
        else:
            context = { "form": form }
            return render(request, 'superhero_app/superhero_create.html', context)

    # GET #
    form = SuperheroForm()
    context = { 'form': form }
    return render(request, 'superhero_app/superhero_create.html', context)