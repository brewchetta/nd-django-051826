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


# GAME #
class Game(models.Model):
    home_team = models.ForeignKey(SportTeam, on_delete=models.CASCADE, related_name='home_games')
    away_team = models.ForeignKey(SportTeam, on_delete=models.CASCADE, related_name='away_games')
    home_score = models.IntegerField()
    away_score = models.IntegerField()

    def __str__(self):
        return f"{self.home_team.name} vs {self.away_team.name}"


# PLAYER #
class Player(models.Model):
    name = models.CharField(max_length=150)
    position = models.CharField(max_length=100)
    team = models.ForeignKey(SportTeam, on_delete=models.CASCADE, related_name='players')

    def __str__(self):
        return self.name