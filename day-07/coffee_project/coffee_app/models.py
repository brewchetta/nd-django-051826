from django.db import models

class Beverage(models.Model):
    name = models.CharField(max_length=100, unique=True)
    caffeinated = models.BooleanField()

    def __str__(self):
        return self.name