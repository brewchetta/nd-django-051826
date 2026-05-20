from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('todos/<int:pk>', views.show_todo, name="show_todo")
]
