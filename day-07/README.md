# Day Seven

## Topics

- Class-Based Views
- ListView
- DetailView
- FormView

## Lesson - Class-Based Views

### Why Use Class-Based Views

In Django a class-based view is one built with a class rather than a function.

One thing that classes have that makes them very powerful is inheritance and mixins. Both inheritance and mixins allow a class to gain behavior from other prebuilt classes and can cut down tremendously on code.

The drawback is that class-based views are less configurable than functional views. Class based and functional views can both exist in the same `views.py` file allowing for mixing and matching based on usecase.

### Template View

The simplest class-based view serves a simple template. Create a template `my_app/about.html`:

```html
<h1>About</h1>

<p>This is a website built with Django</p>
```

Using functional views a developer would create a path that looks like this:

```python
urlpatterns = [
    path("about", views.about)
]
```

...and a view that looks like this:

```python
def about(request):
    return render(request, "my_app/about.html", {})
```

Using a class-based view changes the syntax for the about view:

```python
from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = "my_app/about.html"
```

The `template_name` determines which template will be used for this view and is automatically rendered when the view is called.

The path in `urls.py` will also change slightly:

```python
urlpatterns = [
    path("about", views.AboutView.as_view())
]
```

Because `AboutView` is a class, the `.as_view()` method must be called to activate and it.

### Passing Context

Very often a view requires context to be passed to the template for context specific rendering. In the previous example the context might include information about the website's team:

```python
web_dev_team = [
    {
        "name": "Bob",
        "bio": "I have a passion for making cool websites"
    },
    {
        "name": "Jane",
        "bio": "I love Django!"
    }
]
```

Normally this context can be passed into the render function quickly and easily:

```python
def about(request):
    context = { "web_dev_team": web_dev_team }
    return render(request, "my_app/about.html", context)
```

The template `my_app/about.html` would then be able to hand the context:

```html
{% for dev in web_dev_team %}
<p>{{ dev.name }}</p>
<p>{{ dev.bio }}</p>
{% endfor %}
```

With class based views the method of passing context is also fairly straight forward using the `extra_context` attribute:

```python
from django.views.generic import TemplateView

class AboutView(TemplateView):
    template_name = "my_app/about.html"
    extra_context = { "web_dev_team": web_dev_team }
```

### Handling Different Methods

By default we can create a class based view that handles different requests by giving those requests a name in the view:

```python
class GreetingView(View):
    greeting = "Good Day"

    def get(self, request):
        return HttpResponse(self.greeting)
```

Additionally, specialized views can be connected to models, especially with the introduction of forms:

```python
from django import forms
from .models import Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name']
```

```python
from django.shortcuts import render, redirect
from django.views import View

class ClientFormView(View):
    form_class = ClientForm
    template_name = 'my_app/client_form.html'

    def get(self, request, *args, **kargs):
        form = self.form_class()
        return render(request, self.template_name, { "form": form })

    def post(self, request, *args, **kargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('homepage')
        return render(request, self.template_name, { "form": form })
```

The `.get()` and `.post()` methods will activate depending on the method being used. The class attributes `form_class` and `template_name` ensure the template and form are the same throughout the class but can easily be changed using inheritance:

```python
from django import forms
from .models import VIPClient

class VIPClientForm(forms.ModelForm):
    class Meta:
        model = VIPClient
        fields = ['name', 'vip_perks']
```

```python
class VIPClientFormView(ClientFormView):
    form_class = VIPClientForm
    template_name = 'my_app/vip_client_form.html'
```

The `VIPClientFormView` uses the exact same `.get()` and `.post()` methods as `ClientFormView` however it uses its own `form_class` and `template_name` which have been custom tailored to a vip experience.

### ListView

Django has a pair of specialty views built specifically to show model data. The first is the ListView:

```python
from django.views.generic import ListView
from .models import Client

class ClientListView(ListView):
    model = Client
```

Inside `my_app/client_list.html`:

```html
<h2>Clients</h2>

<ul>
    {% for client in object_list %}
    <li>{{ client.name }}</li>
{% endfor %}
</ul>
```

The `ListView` will automatically create context named `object_list` which includes information from `Client.objects.all()` and pass it to a template named `my_app/client_list.html`. By understanding these assumptions the code makes for them, developers can drastically cut down on code by following certain conventions.

Unfortunately `object_list` isn't a great name for clients so many developers will rename it using the `context_object_name` attribute:

```python
from django.views.generic import ListView
from .models import Client

class ClientListView(ListView):
    model = Client
    context_object_name = "all_clients"
```

```html
<h2>Clients</h2>

<ul>
    {% for client in all_clients %}
    <li>{{ client.name }}</li>
{% endfor %}
</ul>
```

Instead of using the name `objects_list` a developer can now use the more aptly named `all_clients` variable.

The `ListView` also accepts querysets if it's important to filter based on certain conditions:

```python
class ClientListView(ListView):
    context_object_name = "clients"
    queryset = Client.objects.filter(name__icontains="bob")
```

Rather than use all `Client` instances, the `ListView` now finds clients with the name "bob" somewhere in their name.

### DetailView

Similar to the `ListView` which includes data on all `Client` instances, a `DetailView` can show data for a single model instance:

```python
urlpatterns = [
    ...,
    path("clients/<int:pk>", ClientDetailView.as_view())
]
```

```python
from django.views.generic import DetailView
from .models import Client

class ClientDetailView(DetailView):
    model = Client
    context_object_name = "client"
```

```html
<h2>{{ client.name }}</h2>
<p>{{ client.bio }}</p>
```

### FormView

One final generic view that is often used is the `FormView` which handles rendering and submitting forms. Consider this form in `forms.py`:

```python
from django imporrt forms

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'bio']
```

Normally this would require a significant amount of code. However, with the `FormView` that code gets cut significantly:

```python
from .forms import ClientForm
from django.views.generic.edit import FormView

class ClientFormView(FormView):
    template_name = "my_app/client_form.html"
    form_class = ClientForm
    success_url = "/homepage"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
```

This view both renders the initial `ClientForm`, handles re-rendering if there are errors, and will save the new `Client` to the database with its special `.form_valid()` method which triggers when the form has passed validation. The `success_url` determines where the page redirects on completion.

## Recap

There are many more class-based views than what has been shown above. While powerful, a class-based view isn't inherently configurable and rely on certain conventions that might be challenging to remember compared to using functional views. It's ultimately up to the dev to determine whether to use functional or class-based views.

## Exercises