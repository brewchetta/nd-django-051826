from . import views
from django.urls import path

urlpatterns = [
    path('', views.homepage, name="homepage"),
    path('login', views.login, name="login"),
    path('memes', views.memes, name="memes"),

    # dynamic urls - anything in the <> is a variable with a type (int) and a name (num_one)
    path('addition/<int:num_one>/<int:num_two>', views.addition, name="addition"),
    # http://127.0.0.1:8000/addition/12/13
]