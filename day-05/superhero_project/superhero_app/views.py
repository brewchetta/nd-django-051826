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

from django.shortcuts import get_object_or_404

# SUPERHERO EDIT #
def superhero_edit(request, primary_key):
    found_hero = get_object_or_404(Superhero, pk=primary_key)

    # POST #
    if request.method == "POST":
        form = SuperheroForm(request.POST, instance=found_hero)
        if form.is_valid():
            form.save()
            return redirect('superhero_index')
        else:
            context = { "form": form }
            return render(request, 'superhero_app/superhero_edit.html', context)

    # GET #
    form = SuperheroForm(instance=found_hero)
    context = { "form": form }
    return render(request, 'superhero_app/superhero_edit.html', context)

# SUPERHERO DELETE #
def superhero_delete(request, primary_key):
    found_hero = get_object_or_404(Superhero, pk=primary_key)

    # POST #
    if request.method == "POST":
        found_hero.delete()
        return redirect('superhero_index')

    # GET #
    context = { "superhero": found_hero }
    return render(request, 'superhero_app/superhero_delete.html', context)