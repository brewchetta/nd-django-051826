from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Sport
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
    # if request.method == "POST":