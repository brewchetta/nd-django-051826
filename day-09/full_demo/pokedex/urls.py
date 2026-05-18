from django.urls import path
from . import views

urlpatterns = [
    # POKEMON API INFO
    
    path('', views.homepage, name="homepage"),
    
    path('pokemon/<slug:name>', views.pokemon_detail, name="pokemon_detail"),

    path('favorites', views.favorites, name="favorites"),

    # AUTH
    path('signup', views.signup, name="signup"),

    path('login_user', views.login_user, name="login_user"),

    path('logout_user', views.logout_user, name="logout_user")
]