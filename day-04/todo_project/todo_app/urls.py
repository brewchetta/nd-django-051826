from django.urls import path
from . import views

urlpatterns = [
    # TODOS URLS
    path('', views.homepage, name='homepage'),
    path('create-todo', views.create_todo, name="create_todo"),
    path('edit-todo/<int:pk>', views.edit_todo, name="edit_todo"),
    path('delete-todo/<int:pk>', views.delete_todo, name="delete_todo"),

    # TEA URLS
    path('teas', views.tea_index, name="tea_index"),
    path('teas/create', views.tea_create, name="tea_create"),
    path('teas/<int:pk>/edit', views.tea_edit, name="tea_edit"),
    path('teas/<int:pk>/delete', views.tea_delete, name="tea_delete")
]