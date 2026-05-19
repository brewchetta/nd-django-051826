from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('upcoming-movies', views.upcoming_movies, name="upcoming_movies"),
    path('trailer/<int:movie_index>', views.trailer, name="trailer")
]
