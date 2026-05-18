# Day Four

## Topics

- CRUD
- Django Forms
- Django ModelForms
- Handling post requests

## Lesson - CRUD with Models

#### Create

CRUD stands for Create, Read, Update, and Delete. These are the four different things developers can do with data.

With the introduction of models and a database it's important that we know the commands that will cause each of these to trigger.

Assume we have a simple `Client` model which looks like this:

```python
class Client(models.Model):
    name = CharField(max_length=100)
```

In order to create a new instance of a `Client` there are a few different methods:

```python
# First method:
Client.objects.create(name="Bob")

# Second method:
bob = Client(name="Bob")
bob.save()
```

It'll be the second method that makes the biggest difference for later.

#### Read

Reading data has already been covered by the last lesson but here are three quick ways to form a Django `QuerySet` which contains specific data for use:

```python
# all items
Client.objects.all()

# single item based on primary key
Client.objects.get(pk=1)

# one item based on a filter
Client.objects.filter(name__icontains="bob").first()
```

#### Update

The easiest way to update a model is once again to use the `.save()` method:

```python
# create the instance
bob = Client(name="Bob")
bob.save()

# update the instance
bob.name = "Jim"
bob.save()
```

The `.save()` method is context specific, allowing developers to either create a new instance or save an updated instance to the database. In the second case, the updates will overwrite the initial instance.

#### Delete

Deleting a model instance from the database is fairly straightforward:

```python
bob.delete()
```

The `.delete()` method will remove the row from the table and the data will no longer be available in the database.

### Creating Forms

When creating or updating data, Django developers most often require a `<form>` element to be submitted. While they can create the entire form as `html` in a template, it's more common to generate forms using a special class inside a new file `my_app/forms.py`:

```python
from django import forms

class ClientForm(forms.Form):
    name = forms.CharField(max_length=100)
```

The form can then be passed to a view:

```python
# ...other imports
from .forms import ClientForm

def client_create(request):
    form = ClientForm()
    return render(request, "my_app/client_create.html", { "form": form })
```

And inside the `client_create.html` template:

```html
<h2>Add Client</h2>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Submit New Client</button>
</form>
```

The `csrf_token` will generate a special token that gets passed with our submit request. This token enhances security and helps prevent [cross site request forgery](https://owasp.org/www-community/attacks/csrf) attacks. Django requires these tokens by [default](https://docs.djangoproject.com/en/5.2/howto/csrf/) and the request will fail without them.

The syntax `request.as_p` will generate as many input elements as we require for the form. This is context sensitive so the `CharField` will generate `<input type="text" name="name"/>`. When using an `IntegerField` the `type="integer"` and so on and so forth.

Currently when the form is submitted it does not work so the view needs to be altered to accept `POST` requests:

```python
from django.shortcuts import render, redirect
from .forms import ClientForm

def client_create(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            client_name = form.cleaned_data['name']
            new_client = Client(name=client_name)
            new_client.save()
            return redirect('homepage')
        else:
            return render(request, "my_app/client_create.html", { "form": form })

    form = ClientForm()
    return render(request, "my_app/client_create.html", { "form": form })
```

A lot has been added above. The `if` statement determines whether a `POST` request has been submitted. If not, the code starting with `form = ClientForm()` instead renders an empty form on the page.

When a `POST` has been submitted the `ClientForm` can be filled with data from the `POST` request and validated. This determines whether the `POST` data has the proper information or whether a user submitted improper information. For the example above, the `name` needs to exist and be less than 100 characters.

If the form has been validated the name can be picked out of the data and a new client saved to the database. Most often a redirect occurs afterwards. If the form is invalid, the page rerenders and the form will now display errors for the user to correct.

### Using Model Forms

Currently the form in `forms.py` matches the Client model however it creates some repeat code. Compare the below:

```python
# models.py
class Client(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    home_address = models.CharField(max_length=300)
    newsletter_signup = BooleanField(default=False)

# forms.py
class ClientForm(forms.Form):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    home_address = models.CharField(max_length=300)
    newsletter_signup = BooleanField(default=False)
```

This code is not DRY as there's significant repetition which becomes more significant with every additional field added. Django has a special `ModelForm` to cut down on the repetition:

```python
from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'age', 'home_address', 'news_letter_signup']
```

The `Meta` class is a sort of class within a class that determines metadata for certain Django classes, most often related to Django models. In this case the `Meta` class determines which model the form references and which fields to include in the form. Removing the `news_letter_signup` would remove that input from the form when it renders.

With the more robust `ModelForm` the view can also be streamlined:

```python
from django.shortcuts import render, redirect
from .forms import ClientForm

def client_create(request):
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            # the form automatically has functionality to save to the database
            form.save() 
            return redirect('homepage')
        else:
            return render(request, "my_app/client_create.html", { "form": form })

    form = ClientForm()
    return render(request, "my_app/client_create.html", { "form": form })
```

The form knows what model it's connected to and calling the `.save()` method will add the information immediately to the database.

### Updating with Forms

The update will look similar to the create. The exact same form can be used in views if all the same attributes being created can also be updated:

```python
def client_update(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save() 
            return redirect('homepage')
        else:
            return render(request, "my_app/client_create.html", { "form": form })

    form = ClientForm(instance=client)
    return render(request, "my_app/client_create.html", { "form": form })
```

The only major difference between this and the create request is that the update view requires a `Client` instance. Whenever the `ModelForm` is rendered, an instance argument can be passed which determines the default values for the form.

### Deleting With Forms

There are multiple different ways to structure the deletion of data in Django. This example will show how to delete using a confirmation page.

Create a new path for the confirmation page:

```python
urlpatterns = [
    ...,
    path("client/<int:pk>/delete", views.client_delete, name="client_delete")
]
```

The template will be simple:

```html
<p>Are you sure you want do delete {{ client.name }}?</p>
<p>This action cannot be undone.</p>

<form method="post">
    {% csrf_token %}
    <button type="submit">Confirm Deletion</button>
</form>
```

This form will be a simple delete button with a csrf token attached to it. The view will look like this:

```python
def client_delete(request, pk):
    client = get_object_or_404(Client, pk=pk)

    if request.method == "POST":
        client.delete()
        return redirect('homepage')

    return render(request, "my_app/client_delete.html", { "client": client })
```

On a `POST` request confirming deletion, the client gets deleted and a redirect to the homepage occurs.

## Exercises

- Generate a new model from scratch with any number of fields
- Build a view that allows users to see all instances of that model
- Build a view that allows that model to be created
- Build a view that allows that model to be updated
- Build a view that allows that model to be deleted
- In the list view or the base.html add a link to create a new instance
- In the list view add links for each instance to update and delete them
