from rest_framework import serializers
# serializers shape data and choose what we do and don't send when people ask for it
from .models import Sport, SportTeam

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = '__all__' # include everything about the sport


class SportTeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = SportTeam
        fields = ['name', 'location', 'uniform_colors', 'sport']