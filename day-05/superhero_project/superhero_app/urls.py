from django.urls import path
from . import views

urlpatterns = [
    # home path
    path('', views.home, name="home"),
    # superhero paths
    path('superheroes', views.superhero_index, name='superhero_index'),
    path('superheroes/create', views.superhero_create, name='superhero_create'),
    path('superheroes/<int:primary_key>/edit', views.superhero_edit, name="superhero_edit"),
    path('superheroes/<int:primary_key>/delete', views.superhero_delete, name="superhero_delete"),

    # user paths
    path('signup', views.signup, name="signup"),
    path('login', views.login_auth, name="login_auth"),
    path('logout', views.logout_auth, name="logout_auth")
]
