from django.urls import path
from . import views

urlpatterns = [
    # home path
    path('', views.home, name="home"),
    # superhero paths
    path('superheroes', views.superhero_index, name='superhero_index'),
    path('superheroes/create', views.superhero_create, name='superhero_create')
]
