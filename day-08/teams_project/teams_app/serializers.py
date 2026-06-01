from rest_framework import serializers
# serializers shape data and choose what we do and don't send when people ask for it
from .models import Sport, SportTeam, Game, Player

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = '__all__' # include everything about the sport


class SportTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportTeam
        fields = ['id', 'name', 'location', 'uniform_colors', 'sport']


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Game
        fields = '__all__'


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = '__all__'