from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('subtraction/<int:num_one>/<int:num_two>', views.subtraction, name="subtraction")
]
