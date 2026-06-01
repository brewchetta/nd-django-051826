from django.db import models

# SPORT #
class Sport(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# SPORT TEAM #
class SportTeam(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    uniform_colors = models.TextField()
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='sport_teams')

    def __str__(self):
        return self.name
