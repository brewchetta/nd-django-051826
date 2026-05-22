from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('create-todo', views.create_todo, name="create_todo")
]