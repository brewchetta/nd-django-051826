from django.contrib import admin
from .models import PokemonType, Pokemon, Favorite

admin.site.register(PokemonType)
admin.site.register(Pokemon)
admin.site.register(Favorite)