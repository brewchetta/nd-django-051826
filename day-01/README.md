# Day One

## Topics

- What is a web server
- MVC frameworks
- Virtual environment for Python
- `django-admin` and `manage.py`
- Creating routes, views, and templates
- Passing context
- Using `block`, `extends`, and other Django HTML tags
- Dynamic routing with url params

## Lesson - Intro to Django

### Build Virtual Environment

The virtual environment allows users to keep installed packages separated from the global environment. You may need to use `python3` instead of `python` in your commands.

```bash
pip install --upgrade pip   # get latests version of pip
python -m venv venv
source venv/bin/activate    # macOS/Linux only
venv\Scripts\activate       # Windows only
pip install django
```

It's recommended to add a `.gitignore` which excludes `venv`, `__pycache__`, and `*.sqlite3`. For a repo that shares multiple projects you can add that at the root of the repo.

### Initialize Project

```bash
django-admin startproject project_name_here
cd project_name_here
```

Generates a new project in the current directory. Important files include `settings.py` and `urls.py`. Our `manage.py` is a special file we will directly run at times in order to activate special scripts.

The project can be considered the administrative core for Django's web server and then we will add an application (or possibly several applications) to the core project.

You can see the default Django landing page with `python manage.py runserver` and going to http://localhost:8000 in a browser (for students who can't access localhost they should use 127.0.0.1:8000 instead).

### Create New Application

```bash
python manage.py startapp app_name_here
```

The `startapp` script will generate all the files and directories needed for the application. Viewing the major files is recommended. Some files and directories such as `forms.py` and `templates` will need to be built manually depending on the application.

Inside `project_name_here/urls.py`:

```python
INSTALLED_APPS = [
    ...,
    'app_name_here'
]
```

This registers the application with the core project meaning it can now be accessed.

### Configure URL Files

Create a new file named `urls.py` inside of `app_name_here`.

Inside `app_name_here.urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.first_view, name="first_view"),
    path("/path_two", views.second_view, name="second_view")
]
```

Each path or route determines the view activated when someone makes a request for that path. The first argument is the url path itself as a string, the second is the view that are activating, and the optional argument for `name` will be used later for things like `redirect` and the `url` helper.

Inside `project_name_here.urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.sites.urls),
    path('', include('app_name_here.urls'))
]
```

The `include` syntax allows us to incorporate all urls found in `app_name_here/urls.py`, otherwise they won't be included.

## Build Views

You'll generally have to build views for each path added to the `urls.py` with the exception of built in views like the `admin` panel.

A view is part of the application's controller determining what happens when we go to a specific path. This can include serving HTML, processing a form, retrieving or modifying database data, serving JSON data, or even making additional external API calls.

Inside of `app_name_here/views.py` build two basic views:

```python
from django.shortcuts import render

def view_one(request):
    return render(request, "app_name_here/view_one.html")

def view_two(request):
    return render(request, "app_name_here/view_two.html)
```

### Build HTML Templates

These are simple views that will serve an HTML page using the `return render` syntax.

From here we'll need to build out the templates.

Inside `app_name_here/templates` create a new directory named `app_name_here`. We create that inner directory for name spacing purposes; multiple applications might use the same naming conventions so this name spacing helps us keep things separated.

Inside the subdirectory create `view_one.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Django App</title>
</head>
<body>

    <div id="main-container">
        <h1>Welcome to our website!</h1>
    </div>
    
</body>
</html>
```

Create `view_two.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Django App</title>
</head>
<body>

    <div id="main-container">
        <h1>Hello and welcome to another template!</h1>
    </div>
    
</body>
</html>
```

Run the server in the terminal with `python manage.py runserver` at the project's root and navigate to both http://localhost:8000 and http://localhost:8000/view_two.

### Adding a Base Template

Because there's a lot of similar code between the two examples. In order to keep code DRY (Don't Repeat Yourself) we can use a base template.

Create `app_name_here/base.html` inside templates:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Django App</title>
</head>
<body>

    <div id="main-container">
        {% block content %}
        {% endblock %}
    </div>
    
</body>
</html>
```

The template tags `{%%}` are for special programmatic logic including if statements, for loops, and in this case template inheritance.

It's important to emphasize that template tags require both a beginning and ending tag such as `{% block content %}` and `{% endblock %}`.

Change the other templates:

```html
{% extends 'app_name_here/base.html' %}

{% block content %}

<h1>Welcome to our website!</h1>

{% endblock %}
```

The website will look the same however now we can apply code to `base.html` and it will be applied to all templates when they render.

### Adding Context

Create an additional route in `urls.py`:

```python
urlpatterns = [
    ...,
    path("/view_three", views.view_three, name="view_three")
]
```

In this new view in `views.py` we will create and pass context to the template:

```python
def view_three(request):
    context = {
        "greeting": "hello world"
    }
    return render(request, "app_name_here/view_three.html", context)
```

As a side note you may also declare context inline:

```python
return render(request, "app_name_here/addition.html", { "greeting": "hello world" })
```

The context dictionary allows us to pass variables to the template later.

Inside `view_three.html`:

```html
{% extends 'app_name_here/base.html %}

{% block content %}

<p>Current greeting: {{ greeting }}</p>

{% endblock %}
```

The `{{}}` are variable tags which allow us to interpolate the HTML with the value from variables. This will always attempt to parse that variable as a string. The name `greeting` is determined by the context dictionary key.

You may use methods in the variable tags as well but they aren't called with the parentheses:

```html
{% extends 'app_name_here/base.html %}

{% block content %}

<p>Current greeting: {{ greeting.capitalize }}</p>

{% endblock %}
```

### Using Dynamic URLs

Dynamic urls will be more useful in later lessons with the addition of models.

Create a new url:

```python
urlpatterns = [
    ...,
    path("addition/<int:num_one>/<int:num_two>", views.addition, name="addition")
]
```

The `<int:num_one>` syntax means we're expecting an integer in that space and it will get passed to the view, so for example: `localhost:8000/addition/1/2`.

If using text use `<slug:param_name>` instead. Note that text needs to come in the form of a slug: `i-am-a_slug`.

Inside `views.py`:

```python
def addition(request, num_one, num_two):
    context = {
        "num_one": num_one,
        "num_two": num_two,
        "final_result": num_one + num_two,
    }
    return render(request, "app_name_here/addition.html", context)
```

Inside `addition.html`:

```html
{% extends 'app_name_here/base.html %}

{% block content %}

<p>{{ num_one }} + {{ num_two }} = {{ final_result }}</p>

{% endblock %}
```

You can test this route with multiple parameters.

## Exercises

Create a brand new project from scratch being sure to `cd` out of the current one. The instructions for building the new project are available at the base readme.

Inside the project build:

- A `base` view

- A `homepage` view that displays the current date and time (you may have to import something for this)

- A `division` view which accepts two number parameters and divides the first by the second... if the second number is zero, it instead renders a different template that says "ZERO DIVISION ERROR"

## BONUS: Navbar

We can build a navbar using Django's url helper. Inside of `base.html` at a place that makes sense:

```html
<nav>
    <a href="{% url 'view_one' %}">Home</a>
    <a href="{% url 'view_two' %}">Greeting</a>
    <a href="{% url 'view_three' num_one=2 num_two=3 %}">Add 2 + 3</a>
</nav>
```

Notice that the url helper needs the name determined by `urls.py`, otherwise it will try to use the name of the first view it finds with a matching name.

For url parameters, we add key/value pairs after the name of the route.

## BONUS: For Loops and Accessing Dictionary Information

Create a url path and a view named `todo_list`:

```python
def todo_list(request):
    context = {
        my_list: [
            { "description": "Walk dog", "priority": "1" },
            { "description": "Do laundry", "priority": "3" },
            { "description": "Buy groceries", "priority": "2" },
        ]
    }
    return render(request, 'app_name_here/todo_list.html', context)
```

Inside `todo_list.html`:

```html
{% extends 'app_name_here/base.html %}

{% block content %}

<h2>My Todo List</h2>

{% for item in my_list %}

    <p>{{ item.description }} | Priority: {{ item.priority }}</p>

{% endfor %}

{% endblock %}

```

This `for` loop works just like in normal python with the exception that we need a closing tag for it. When accessing keys in a dictionary, use dot notation instead of `.get` or bracket notation.