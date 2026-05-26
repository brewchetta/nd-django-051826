from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# SUPERHERO #
class Superhero(models.Model):
    alias = models.CharField(max_length=100)
    real_name = models.CharField(max_length=100)
    powers = models.TextField()
    origin_story = models.TextField()
    # user association
    # the user can be null a.k.a. deleted
    user = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="superheroes", null=True, blank=True)

    def __str__(self):
        return self.alias

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)