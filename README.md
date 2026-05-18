# Python Django Immersive

## Commands To Get Started

Follow the commands below to get started on a django project. Look at the various day files to get a sense for how to do specific actions such as dynamic url paths, databases, etc.

### Build Virtual Environment

```bash
python -m venv venv
source venv/bin/activate    # macOS/Linux only
venv\Scripts\activate       # Windows only
pip install django
```

### Initialize Project

```bash
django-admin startproject project_name_here
cd project_name_here
```

### Create New App

```bash
python manage.py startapp app_name_here
```

Inside `project_name_here/urls.py`:

```python
INSTALLED_APPS = [
    ...,
    'app_name_here'
]
```

### Configure URL Files

Inside `app_name_here.urls.py`:

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.path_one, name="path_one"),
    path("/path_two", views.path_two, name="path_two")
]
```

Inside `project_name_here.urls.py`:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.sites.urls),
    path('', include('app_name_here.urls'))
]
```

### Build Views

From here you may build your views following best practices.

## Lessons

- [Day One - Intro to Django](./day-01/)

- [Day Two - Mini Project w/ Static Files](./day-02/)

- [Day Three - Django Models](./day-03/)

- [Day Four - CRUD with Models](./day-04/)

- [Day Five - Authentication and Authorization](./day-05/)

- [Day Six - Mini-Project w/ File Uploads](./day-06/)

- [Day Seven - Class-Based Views](./day-07/)

- [Day Eight - Django As An API](./day-08/)

- [Day Nine - Capstone Project](./day-09/)

- [Day Ten - Capstone Project](./day-10/)