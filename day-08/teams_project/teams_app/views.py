from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Sport, SportTeam, Game
from rest_framework.response import Response
from rest_framework import status

from .serializers import SportSerializer

# api/v1/sports
@api_view(['GET', 'POST']) # this decorator makes it so we can only use GET and POST requests
def sport_list(request):

    # GET # 
    # send back all the sports we have
    if request.method == "GET":
        all_sports = Sport.objects.all()
        # make items into dictionaries
        serializer = SportSerializer(all_sports, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST #
    # accepts information for a new sport and create in the database
    if request.method == "POST":
        new_data = request.data # this is how we capture the info the user sent
        serializer = SportSerializer(data=new_data)
        if serializer.is_valid():
            # add to the database
            serializer.save()
            # send receipt that everything went well
            return Response(serializer.data, status=status.HTTP_201_CREATED) # 201 for created
        else:
            # let user know something went wrong
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # 400 bad data
        

from .serializers import SportTeamSerializer

# /api/v1/sport_teams
@api_view(['GET', 'POST']) # only get and post
def sport_team_list(request):

    # GET
    if request.method == "GET":
        all_teams = SportTeam.objects.all() # get all teams
        serializer = SportTeamSerializer(all_teams, many=True) # serialize teams
        return Response(serializer.data, status=status.HTTP_200_OK) # send response

    # POST
    if request.method == "POST":
        serializer = SportTeamSerializer(data=request.data) # serialize the request data
        if serializer.is_valid(): # validate the data
            serializer.save() # if valid, save and return
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # otherwise handle errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# /api/v1/sport_teams/:pk
@api_view(['GET', 'PATCH', 'DELETE'])
def sport_team_detail(request, pk):

    # grab team based on pk
    try: # try to get the team based on pk
        team = SportTeam.objects.get(pk=pk) # <<< this might break and cause an error
    except SportTeam.DoesNotExist: # if there was an error bc the team doesn't exist...
        return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    # GET #
    if request.method == "GET":
        serializer = SportTeamSerializer(team) # serialize the found team
        return Response(serializer.data, status=status.HTTP_200_OK) # send it to client

    # PATCH #
    if request.method == 'PATCH':
        serializer = SportTeamSerializer(team, data=request.data) # create a serializer with the team data and the edit data
        if serializer.is_valid(): # check if valid
            serializer.save() # save changes to db
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED) # return changed data
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) # otherwise return errors

    # DELETE #
    if request.method == 'DELETE':
        team.delete() # delete the item
        return Response(status=status.HTTP_204_NO_CONTENT) # send an empty response


# /api/v1/games
# /api/v1/games/:id
# using a very fancy class based view that does all the heavy lifting
from rest_framework import viewsets
from .serializers import GameSerializer
class GameViewset(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer


# PLAYER VIEWS #

from rest_framework.views import APIView
from .models import Player
from .serializers import PlayerSerializer

class PlayerListView(APIView):

    # GET #
    def get(self, request):
        players = Player.objects.all()
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST #
    def post(self, request):
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
from django.http import Http404

class PlayerDetailView(APIView):

    def get_player(self, pk):
        try:
            return Player.objects.get(pk=pk)
        except Player.DoesNotExist:
            raise Http404

    # GET #
    def get(self, request, pk):
        player = self.get_player(pk)
        serializer = PlayerSerializer(player)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # PATCH #

    # DELETE #