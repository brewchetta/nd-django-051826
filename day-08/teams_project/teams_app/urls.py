from django.urls import path
from . import views

urlpatterns = [
    # url for seeing all sports & creating new sports
    path('api/v1/sports', views.sport_list, name="sport_list"),
    # path('api/v1/sports/<int:id>', views.sport_detail, name="sport_detail"),

    # urls for all teams, creating teams
    path('api/v1/sport_teams', views.sport_team_list, name="sport_team_list"),
    # urls for seeing a team, editing a team, deleting a team
    path('api/v1/sport_teams/<int:pk>', views.sport_team_detail, name="sport_team_detail"),
]

# RESTful conventions
# GET       /sports --> read all the sports
# POST      /sports --> create a new sport
# GET       /sports/:id --> read a specific sport
# PATCH     /sports/:id --> edit a specific sport
# DELETE    /sports/:id --> delete a specific sport