from . import views
from django.urls import path

urlpatterns = [
    path('', views.homepage),
    path('login', views.login),
    path('memes', views.memes)
]