# Day Six

## Topics

- Mini Project

## Deliverables

- Generate user stories
- Generate a new project and app
- Add a homepage and `base.html`
- Incorporate the User model
- Create at least 2 models, one of which has a relationship
- Create full CRUD on at least one model
- Create a login / signup / logout for the user model

## BONUS: Uploading Files & Images

Images and files may be attached to a model and uploaded with some setup in development.

Inside `my_project/settings.py`:

```python
# ...other imports
import os

# ...other settings items

STATIC_URL = "static/"

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'
```

This signifies that we want a `media/` directory to store our media, at least in development mode.

Inside `my_project/urls.py`:

```python
# ...other imports
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    ...
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

This adds a new special path whenever `DEBUG` has been set to true in the settings to allow access to the `media/` directory as a static path for images.

Create a new model:

```python
class Cat(models.Model):
    name = CharField(max_length=100)
    image = models.ImageField(upload_to="cat_images", blank=True, null=True)
```

The image will now automatically get added to `media/cat_images/` when passed along by a form. The form needs a special attribute to allow for images/files to be sent:

```html
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Submit</button>
</form>
```

The `enctype` enables image and file data to be sent along with the any other necessary data.

Finally one last change needs to be made in the view to allow image data:

```python
def cat_create(request):
    if request.method == "POST":
        form = CatForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('homepage')

    return render(request, 'my_app/cat_create.html', { "form": CatForm() })
```

Because the request now includes file data in addition to post data, the view now accounts for that.