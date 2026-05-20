from django.contrib import admin
from .models import Todo, Author, Book

admin.site.register(Todo)
admin.site.register(Author)
admin.site.register(Book)