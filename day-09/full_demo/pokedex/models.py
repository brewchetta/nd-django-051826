from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class PokemonType(models.Model):
    name = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class Pokemon(models.Model):
    name = models.CharField(max_length=100)
    pokemon_id = models.IntegerField()
    pokemon_types = models.ManyToManyField(PokemonType, blank=True)

    def __str__(self):
        return self.name

class Favorite(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="favorites")
    caught = models.BooleanField()

    def __str__(self):
        return f"{self.pokemon.name} - {self.user.username}"

# User ----< Favorite >---- Pokemon ---<>--- PokemonType