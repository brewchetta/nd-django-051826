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

from .forms import SignUpForm
from django.contrib.auth import login

# SIGNUP #
def signup(request):
    # POST #
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            # form.save returns the new user
            user = form.save()
            # login will send a session cookie to the user to represent them being logged in
            login(request, user)
            return redirect('home')
        else:
            context = { "form": form }
            return render(request, 'superhero_app/signup.html', context)

    # GET #
    context = { "form": SignUpForm() }
    return render(request, 'superhero_app/signup.html', context)
    
from .forms import LoginForm
from django.contrib.auth import authenticate

# LOGIN #
def login_auth(request):
    # POST #
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            # get the username & password from the validated form
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # authenticate checks that the user exists and has this password
            user = authenticate(request, username=username, password=password)
            if user:
                # if user exists then log them in
                login(request, user)
                return redirect('home')
        context = { 'form': form, 'error': 'Invalid username or password' }
        return render(request, 'superhero_app/login.html', context)

    # GET #
    context = { 'form': LoginForm() }
    return render(request, 'superhero_app/login.html', context)

from django.contrib.auth import logout

# LOGOUT #
def logout_auth(request):
    # logout the user by deleting the session cookie
    logout(request)
    return redirect('home')