from django.db import models

# SUPERHERO #
class Superhero(models.Model):
    alias = models.CharField(max_length=100)
    real_name = models.CharField(max_length=100)
    powers = models.TextField()
    origin_story = models.TextField()

    def __str__(self):
        return self.alias

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)