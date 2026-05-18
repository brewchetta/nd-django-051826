# Day Three

## Topics

- Django models
- MVC frameworkers
- Model fields
- Creating superusers
- Admin panel
- Model associations

## Lesson - Django Models

### What is a Model

Django is an MVC framework (MVC = Model View Controller). A controller determines what actions different routes take and a view is the specific action including specific rendering for a route. But what about a model?

Web servers are often linked to databases and rather than writing SQL directly, many will use a special layer known as an ORM (object relational manager) to build its Models. A model in Django is an abstraction for a SQL table, an object that runs SQL code so the developer doesn't have to. In effect, a Model is the link to the database.

### Creating and Migrating Simple Models

Create a new project and app using `django-admin` and `manage.py`.

Inside `my_app/models.py` you'll be able to begin defining your models. We can start simply:

```python
from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
```

The new class `Author` inherits a host of methods and attributes from Django's special `Model` class. The `Author` will technically have two columns in its table: 
- a `first_name` and `last_name` as a small string with a maximum length of 100 characters
- an `id` which is the primary key for the `Author` table which gets created automatically

The `__str__` dunder method displays the name of the author when it's shown as a string.

While Django will create a `db.sqlite3` by default, it hasn't be structured yet. A migration must be created and applied to the table.

Use the following commands in the terminal at the location of `manage.py`:

```bash
python manage.py makemigrations
python manage.py migrate
```

Notice that `makemigrations` will add a new file to the `my_app/migrations/` directory named `0001_initial.py`. Look through the migration file for an idea about what it includes. When we `migrate` it will actually add the table to the SQL database.

Run the two commands whenever making new changes to `models.py`.

### Using the Admin Panel

Firstly we must register the new models for the admin panel. Inside `my_app/admin.py`:

```python
from django.contrib import admin
from .models import Author

admin.site.register(Author)
```

Django by default has a special set of routes and views for administrators to manage model data. Before using the admin panel create a super user in the terminal:

```bash
python manage.py createsuperuser
```

The terminal will now ask a series of questions to create the superuser for your project. You must include username and password but you may leave the other areas blank. Since this is a development project it's recommended you use a simple username / password like `admin` and `123`.

Once the superuser has been created run the server with:

```bash
python manage.py runserver
```

Navigate to http://localhost:8000/admin and login with the credentials just created. The `Author` model should be apparent.

Click the `Add` button in order to add a new `Author`. Submit as many authors as preferred.

### Accessing Models in Views

Create a new view such as a `/authors` page. Previously, context required hardcoded information however the `Author` model allows data fetched from an active database.

For the view function:

```python
from django.shortcuts import render
from .models import Author

def author_list(request):
    all_authors = Author.objects.all()
    context = { "authors": all_authors }
    return render(request, "my_app/author_list.html", context)
```

The `Author.objects` attribute gives access to authors in the database using certain chained methods. This returns a special object known as a `QuerySet`.

Inside the html:

```html
<ul>
{% for author in all_authors %}

<li>{{ author.first_name }} {{ author.last_name }}</li>

{% endfor %}
</ul>
```

Run the server and navigate to the page. The author names should be present.

### Accessing Models By Id

Models can also be accessed via their id. Create a new dynamic url in `urls.py`:

```python
urlpatterns = [
    ...,
    path("authors/<int:primary_key>", views.author_detail, name="author_detail")
]
```

Inside the view:

```python
def author_detail(request, primary_key):
    author = Author.objects.get(pk=primary_key)
    context = { "author": author }
    return render(request, "my_app/author_detail.html", context)
```

Inside the html:

```html
<h1>{{ author.first_name }} {{ author.last_name }}</h1>
<h2>ID: {{ author.id }}</h2>
```

While the server is running navigate to http://localhost:8000/authors/1 where an author should be seen.

Currently this route is brittle, navigating to http://localhost:8000/authors/10000 (assuming you haven't created 10000 Authors) will result in an error. 

You can alter the view function to account for the potential error which will give Django's default 404 page instead:

```python
# other imports...
from django.shortcuts import get_object_or_404

# ...

def author_detail(request, primary_key):
    author = get_object_or_404(Author, pk=primary_key)
    context = { "author": author }
    return render(request, "my_app/author_detail.html", context)
```

The `get_object_or_404` function operates similar to `.objects.get()` with the exception of causing a 404 error when it cannot find the item.

### Model Associations - ForeignKey

Since SQL is a relational database it has been built to allow table associations through something special known as a "foreign key". For example, with an author table and a book table, a book can belong to a specific author by giving the book a foreign key. If Gabriel Garcia Marquez has an `id` of `1` (the author's primary key), every book with an author foreign key of 1 belongs to Gabriel Garcia Marquez.

Django handles most, a developer just needs to add a special field to `models.py`:

```python
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.Charfield(max_length=200)
    page_count = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
```

Don't forget to run the `makemigrations` and `migrate` commands.

Register the new book model in `my_app/admin.py`:

```python
from django.contrib import admin
from .models import Author, Book

admin.site.register(Author)
admin.site.register(Book)
```

Run the server and navigate to `http://localhost:8000/admin` and create books. Those books must be associated with an already created author.

The optional `on_delete=models.CASCADE` argument causes all of an author's books to be deleted when that author gets deleted.

The optional `related_names=books` argument grants a `books` attribute to authors so that an author can access their books. For example:

```python
author_1 = Author.objects.get(pk=1)
author_1_books = author_1.books.all()
```

We can use this in the `author_detail` template:

```html
<h1>{{ author.name }}</h1>
<p>ID: {{ author.id }}</p>

<h2>Books Written: </h2>
{% for book in author.books.all %}
<p>{{ book.title }}</p>
{% endfor %}
```

### Model Associations - ManyToManyField

Consider the concept of books and genres. A book can belong to multiple genres and a genre can encompass many books. This is considered a "many to many" relationship whereas a book belonging to a single author is a "one to many" relationship.

Django makes many to many relationships fairly straightforward:

```python
class Genre(models.Model):
    name = models.CharField(max_length=50)

class Book(models.Model):
    title = models.Charfield(max_length=200)
    page_count = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    genres = models.ManyToManyField(Genre, blank=True)
```

Be sure to `makemigrations` and `migrate`.

A book may now associate with multiple genres. The `blank=True` allows a book to have no associated genres. Most fields allow for the optional `blank=True` and `null=True` arguments let them have empty data in the database. By default, anything that doesn't have these will be a required attribute and will not accept null values.

You may now generate genres in the admin panel and edit books to have genres.

## Exercises

Create four new models:

- A Library model with attributes `name` as text
- A Librarian model with attributes `name` as text, `salary` as an integer, `date_hired` as a datetime, and `library` as a foreignkey for `Library`
- A Customer model with attributes `name` as text, `favorite_libraries` as a many to many with `Library`

## BONUS: Field Types

Django has multiple different fields to explore which determines the data types for its models. Examples that will feel familiar are the CharField, TextField, IntegerField, FloatField, and BooleanField. There are also the [EmailField](https://docs.djangoproject.com/en/6.0/ref/models/fields/#emailfield), [SlugField](https://docs.djangoproject.com/en/6.0/ref/models/fields/#slugfield), and [URLField](https://docs.djangoproject.com/en/6.0/ref/models/fields/#urlfield) which can be read about.

There is also a DateField and a DateTimeField which allow for python `datetime` objects. They allow for two special optional arguments:

```python
class Item(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

The `auto_now_add` automatically fills the date/time with the current timestamp when first created and `auto_now` automatically fills it when it has been altered at all. The `created_at` and `updated_at` fields are common fields across all models.

The DecimalField can be helpful for specifying more precise fixed point numbers in regards to currency.

```python
class Item(models.Model):
    price = DecimalField(decimal_places=2, max_digits=5)
```

In the example the `decimal_places` argument ensures there will only be 2 decimal places allowed.

The `max_digits` argument determines the overall maximum number of digits that are allowed by the field and goes hand in hand with `decimal_places`.

In addition, many fields can include special optional arguments that alter their behavior:

```python
class Item(models.Model):
    name = CharField(unique=True)
    description = TextField(blank=True, null=True)
```

When `unique=True` the field cannot match something already in the database, for example there can't be two items with the name `"refrigerator"`.

When `blank=True` and `null=True` a field may be blank. By default all fields are required until they have these arguments.

## BONUS: Query Params and Filters

Any url can allow for something known as a query parameter. An example of a url with two query params:

```
http://localhost:8000/authors?first_name=Gabriel&last_name=Marquez
```

In a way a query parameter works similarly to a python function with key word arguments. In the example, `first_name` will be `Gabriel` and `last_name` will be `Marquez`.

Inside of a view we can access and use query params to find and filter authors:

```python
def author_list(request):
    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')
    authors_query_set = Author.objects
    
    if first_name:
        authors_query_set = authors_query_set.filter(first_name=first_name)
    if last_name:
        authors_query_set = authors_query_set.filter(last_name=last_name)

    context = { "authors": authors_query_set.all() }
    
    return render(request, "my_app/authors_list.html", context)
```

Because query params are optional, the request.GET dictionary object requires us to `.get` the value from it. 

The query set containing authors can be filtered multiple times if desired. Each filter takes an argument of an attribute for the model.

Currently this works well when an author's first or last name is type in exactly but `first_name=gabriel` or `last_name=Marq` would both fail since they are improperly cased or incomplete. The filter can be altered to accommodate:

```python
if first_name:
    authors_query_set = authors_query_set.filter(first_name__iexact=first_name)
if last_name:
    authors_query_set = authors_query_set.filter(last_name__contains=last_name)
```

The `first_name__iexact` and `last_name__contains` are special arguments that find based on looser filter conditions. The `__iexact` allows for a case insensitive search while `__contains` will show all names that contain the substring given.

These can be combined:

```python
if first_name:
    authors_query_set = authors_query_set.filter(first_name__icontains=first_name)
if last_name:
    authors_query_set = authors_query_set.filter(last_name__icontains=last_name)
```

These now both filter and search for case insensitive partial substrings. Using the url `http://localhost:8000/authors?first_name=g&last_name=m` would now find Gabriel (Garcia) Marquez.
