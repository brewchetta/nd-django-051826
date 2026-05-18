# Day Five

## Topics

- User model
- Authentication routes
- Authorization

## Lesson - Authentication and Authorization

### Adding User Models

By default a user model will be added to new projects. Inside `settings.py` there should already be a number of user and auth related applications being included in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    "django.contrib.auth",
    ...
]
```

This particular application autmoatically adds special authentication and user related items. Using the `makemigrations` and `migrate` commands will automatically add the `User` model to the database.

Create a superuser and navigate to the admin panel. Under the users tab the superuser should already be visible although other users can be generated. Each user requires a username and password. Passwords are automatically encrypyed with a special process known as salting and hashing, Django handles this complex cryptography process where other frameworks might more ask devs to engineer them manually.

### Creating a User Signup

The user signup requires a specialized form called the `UserCreationForm`:

```python
# ...other imports
from django.contrib.auth.forms import UserCreationForm

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
```

The `password1` and `password2` fields are for password confirmation. Email isn't strictly required. Both username and password will have strict validations requiring real and unique usernames and passwords.

Utilize the form as normal to be rendered in the view and html:

```python
from .forms import SignUpForm

def signup(request):
    form = SignUpForm()
    return render(request, 'my_app/signup.html', { "form": form })
```

```html
<h1>Signup</h1>

<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Submit</button>
</form>
```

Navigating to the page will render the form however submitting it won't cause anything to happen. This can be fixed by altering the view:

```python
# ...other imports
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login

def signup(request):
    if method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('homepage')
        else:
            return render(request, 'my_app/signup.html', { "form": form })
    form = SignUpForm()
    return render(request, 'my_app/signup.html', { "form": form })
```

This looks similar to previous form submissions however it also includes this special `login` function. When activated with a valid user argument the function will generate something known as a session cookie in the browser. This data will now be passed along with every request which allows Django to know who the currently logged in user is.

Any template may use this information:

```html
{% if request.user.is_authenticated %}
<p>Currently logged in: {{ request.user.username }}</p>
{% endif %}
```

The `request.user` object accesses the User that has been logged in with the `login` function if they exist. The `is_authenticated()` method determines whether a user is currently logged in or "authenticated".

### Creating a User Logout

Once a user has been signed up they require a way to log out. The logout process is fairly straightforward requiring a new path and a new view:

```python
# ...other imports
from django.shortcuts import render, redirect
from django.contrib.auth import logout

def logout_user(request):
    logout(request)
    return redirect('homepage')
```

This route will clear out the session cookie with user information effectively logging them out:

```html
<a href="{% url 'logout_user' %}">Logout</a>
```

### Creating a User Login

If an existing user has been logged out the final step will be allowing login. Inside of `forms.py` add the additional form:

```python
# ...other imports
from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)
```

The widget argument alters the form html for the input, in this case causing the password to have a `type="password"` for its input. This will obscure the password when people type into the field.

The view will be slightly altered from a normal model view:

```python
# ...other imports
from .forms import LoginForm
from django.contrib.auth import login, logout, authenticate

def login_user(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                redirect('homepage')
        return render(request, 'my_app/login_form.html', { "form": form })

    form = LoginForm()
    return render(request, 'my_app/login_form.html', { "form": form })
```

The login will check that the form is valid before also finding a user with `authenticate`, a function which tests a user and their password against the database. If they are authenticated, they login and otherwise the form gets re-rendered.

As a final touch the `base.html` can include an additional section that will either show links to signup/login or to logout:

```html
<div class="auth-section">
    {% if request.user.is_authenticated %}
        <span>Logged in as {{ request.user.username }}</span>
        <a href="{% url 'logout' %}">Logout</a>
    {% else %}
        <a href="{% url 'login_user' %}">Login</a>
        <a href="{% url 'signup' %}">Sign up</a>
    {% endif %}
</div>
```

### Login Required Views

Django allows views to be access blocked using a special decorator. For example, if a user created a `profile` view, it would make sense only an authenticated user could access it:

```python
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    context = { "current_user": request.user }
    return render(request, "my_app/profile.html", context)
```

The `@login_required` decorator will prevent users who aren't currently logged in from accessing the page at all. The profile will also always show the current user's details as opposed to the details of any other users. This can be further modified with model associations:

```python
from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    context = { 
        "current_user": request.user, 
        "favorite_books": request.user.books
    }
    return render(request, "my_app/profile.html", context)
```

## Exercises

In either a fresh project or a previous project implement the following:

- a user model
- a user signup
- a user login
- a user logout
- a heading in the `base.html` which will show links based on whether a user is logged in or logged out
- a profile only accessible when logged in which shows the current user's information

## BONUS: Extended User Models

At times a user requires additional attributes. These can include profile pictures, a biography, or something else.

In order to "extend" the user a one to one relationship can be made with another model in `models.py`:

```python
# ...other imports
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    biography = models.TextField(blank=True, null=True)
    user = OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
```

The `OneToOneField` creates a direct connection between the `User` and the `Profile`. Deleting the User also deletes the Profile however a Profile hasn't been created by default.

The `User` is accessed with the special `get_user_model()` function which is more predictable than importing the `User` directly since the `User` can be modified in different ways.

## BONUS: Signals and Receivers

After implementing the above it may make sense to allow Django to automatically create a linked `Profile` whenever a `User` gets created. Django does this through a "signals" system.

You'll most likely add this at the end of `models.py`: 

```python
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
```

The `@receiver` decorator knows that it's looking for a `.save` from a model to our database and that this specifically happens with our `User` model. When we save a `User` it will activate our `create_user_profile` which creates a new associated `Profile` when the user gets created.

Signals and receivers can happen in a variety of other circumstances as well. Consider this one from the [Django docs](https://docs.djangoproject.com/en/1.11/topics/signals/#django.dispatch.receiver):

```python
from django.core.signals import request_finished
from django.dispatch import receiver

@receiver(request_finished)
def my_callback(sender, **kwargs):
    print("Request finished!")
```

This receiver will trigger every time that a request is finished which means we can perform certain functions after each request.
