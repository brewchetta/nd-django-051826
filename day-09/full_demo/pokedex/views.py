from django.shortcuts import render, redirect
import requests
from .forms import SignUpForm, LoginForm, SearchForm, FavoriteForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import PokemonType, Pokemon, Favorite

POKE_API_BASE_URL = "https://pokeapi.co/api/v1/"

def homepage(request):
    # if someone is making a POST to the homepage
    # they have triggered our search form!
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            # grab 'name' out of the form
            pokemon_name = form.cleaned_data['name']
            return redirect('pokemon_detail', name=pokemon_name)
    try:
        # fetch from the pokeapi and add that to context for the page
        response = requests.get(POKE_API_BASE_URL + "pokemon?limit=151")
        # parse the json body from the response
        parsed_response = response.json()
        # add the results to context
        context = { 
            "pokemon_list": parsed_response.get('results'),
            "form": SearchForm()
        }
    except Exception as error_message:
        context = {
            "pokemon_list": [],
            "errors": str(error_message),
            "form": SearchForm()
        }
    # render
    return render(request, "pokedex/homepage.html", context)

def pokemon_detail(request, name):
    # this is the post request for the favorite form
    if request.method == "POST":
        form = FavoriteForm(request.POST)
        print("we have the form")
        if form.is_valid():
            # get pokemon name and find that pokemon in db
            name = form.cleaned_data['name']
            pokemon = Pokemon.objects.filter(name=name).first()
            # if found just mark it in db as favorite
            if pokemon:
                # just favorite it
                fav = Favorite(pokemon=pokemon, user=request.user, caught=False)
                fav.save()
                return redirect('homepage')
            # if not found we need create the pokemon and favorite
            else:
                # make and save pokemon
                pokemon = Pokemon(
                    name=name, 
                    pokemon_id=form.cleaned_data['pokemon_id'],
                )
                pokemon.save()
                # make and save
                fav = Favorite(pokemon=pokemon, user=request.user, caught=False)
                fav.save()
                return redirect('homepage')
    try:
        response = requests.get(POKE_API_BASE_URL + "pokemon/" + name)
        parsed_response = response.json()
        # pokemon type name is us using list comprehension to get the individual names
        pokemon_type_names = [ t['type']['name'] for t in parsed_response.get('types') ]
        print(pokemon_type_names)
        # from the names we find the individual type in the db
        pokemon_types = [ PokemonType.objects.filter(name=name).first() for name in pokemon_type_names ]
        # generate initial form data for pokemon
        initial_data = { 
            'name': parsed_response['name'],
            'pokemon_id': parsed_response['id'],
            'pokemon_types': pokemon_types
        }
        form = FavoriteForm(initial=initial_data)
        context = { "pokemon": parsed_response, "form": form }
    except Exception as error_message:
        context = {
            "pokemon": {},
            "errors": str(error_message)
        }
    # render
    return render(request, "pokedex/pokemon_detail.html", context)

@login_required
def favorites(request):
    # get all user's favorites
    favorite_pokemon = request.user.favorites.all()
    context = { "favorite_pokemon": favorite_pokemon }
    return render(request, 'pokedex/favorites.html', context)

# AUTH

def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login will login the user
            login(request, user)
            return redirect('homepage')
        else:
            context = { 
                "form": form, 
                "header": "Sign up for Pokemon Goodness!!!" 
            }
            return render(request, "pokedex/signup.html", context)
    else: 
        # GET / any other method
        form = SignUpForm()
        context = { 
            "form": form,
            "header": "Sign up for Pokemon Goodness!!!"
        }
        return render(request, "pokedex/user_form.html", context)
    
def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # look up the user by username and check to see if encrypting the password in the form generates the same encrypted password in the database
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('homepage')
        # we will only get to this next line if we don't hit the line above
        context = { 
            "form": form,
            "header": "Login",
            "errors": "Invalid username or password"
        }
        return render(request, 'pokedex/user_form.html', context)
    else:
        form = LoginForm()
        context = { 
            "form": form,
            "header": "Login"
        }
        return render(request, 'pokedex/user_form.html', context)

def logout_user(request):
    logout(request)
    return redirect('homepage')