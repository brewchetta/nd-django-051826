from django.urls import path, include
from . import views
from rest_framework import routers

# the api_path prefix allows us to keep all prefixes the same and is easily changed
API_PATH = 'api/v1/'
# it's best to use /api/v1 to show these routes are for the api and they belong to a specific version
# versioning like this makes it easier to create deprecated routes later

# ROUTERS --- USED W/ VIEWSETS ###################################
router = routers.DefaultRouter()
router.register(r"api/v1/games", views.GameViewset)
##################################################################

urlpatterns = [
    # url for seeing all sports & creating new sports
    path(API_PATH + 'sports', views.sport_list, name="sport_list"),
    # path('api/v1/sports/<int:id>', views.sport_detail, name="sport_detail"),

    # urls for all teams, creating teams
    path(API_PATH + 'sport_teams', views.sport_team_list, name="sport_team_list"),
    # urls for seeing a team, editing a team, deleting a team
    path(API_PATH + 'sport_teams/<int:pk>', views.sport_team_detail, name="sport_team_detail"),

    # urls for all games, creating games
    # urls for individual games, editing, deleting
    path("", include(router.urls)),

    # urls for all players, creating players
    path(API_PATH + 'players', views.PlayerListView.as_view()),
    # urls for individual players, editing, deleting
    path(API_PATH + 'players/<int:pk>', views.PlayerDetailView.as_view()),
]

# RESTful routing conventions
# GET       /sports --> read all the sports
# POST      /sports --> create a new sport
# GET       /sports/:id --> read a specific sport
# PATCH     /sports/:id --> edit a specific sport
# DELETE    /sports/:id --> delete a specific sport