# Day Eight

## Topics

- djangorestframework

## Lesson - Django As An API

### Why Build An API

In programming an API often refers to a remote server that sends and receives information without sending view data. APIs decoupled from views allows the informational layer to be discretely maintained by a dedicated team.

### The Django Rest Framework

The `djangorestframework` library allows devs to create an API through Django that serves information in non-HTML formats like JSON.

To begin, create a virtual environment and then install the new library:

```bash
pip install djangorestframework
```

From here build the project and application boilerplate being sure to hold off on building the views until you are ready.

Inside the project's `settings.py` modify the installed apps:

```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    ...
]
```

This will inform the project that you have the required library. Also ensure your newly created app has been added as well.

At this point construct models in the `models.py` file. These can be as simple or complex as required.

Run your migrations with:

```python
python manage.py makemigrations
python manage.py migrate
```

### Creating A Serializer

In Django and many other frameworks a serializer determines what the data you send as JSON will look like, effectively it's "shape".

Create a file `serializers.py` for your app:

```python
from rest_framework import serialziers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'
```

The `Meta` class lets the serializer know which model we're affecting and which of its attributes or fields to include, in this case all of them. You can amend the serializer to only use specific fields as well:

```python
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["name", "price"]
```

You may manually see how a serializer works by selecting an item from the database and passing it as an argument to the serializer:

```python
serializer = ItemSerializer(item_1)
```

### Creating Views

You app may now serve views which are in fact serialized JSON data. The easiest way to serve a set of views is with a special `ModelViewSet` class:

```python
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Item
from .serializers import ItemSerializer

@api_view(["GET","POST"])
def item_list(request):
    if request.method == "GET":
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return RESPONSE(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PATCH", "DELETE"])
def item_detail(request, pk):
    try:
        item = item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # GET REQUEST
    if request.method == "GET":
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    # PATCH REQUEST
    elif request.method == "PATCH":
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # DELETE REQUEST
    elif request.method == "DELETE":
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

The `@api_view` syntax is a special function known as a `decorator` which modifies the function that follows it. In this case it change a few things about the view including only allowing it to accept certain response methods.

Finally, the `urls.py` needs information on how to route to these special viewsets:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("items/", views.items_list),
    path("items/<int:pk>/", views.item_detail)
]
```

We have successfully built a set of views for our items! We may now use these routes and methods:

```
GET     /items
GET     /items/:id
POST    /items
PATCH   /items/:id
DELETE  /items/:id
```