# Day Two

## Topics

- User stories
- Static files
- Project planning
- Mini project

## Lesson - Mini Project

### Creating User Stories

Today you'll be building a mini-project. 

Before getting started on the project you'll need to create a plan. Most often, developers will determine what they need to do based on various criteria such as "user stories". A user story is formatted as "persona" + "need" + "purpose" and helps the team (in this case you) determine the who, what, and why behind a piece of functionality.

Example user stories: 

`"A client will be able to log in so that they can access their content."`
`"An admin will be able to ban disruptive users in order to maintain community standards."`
`"A guest user will be able to see a feed of the content with only a preview of premium items to entice users"`

User stories are generally informal however they give developers a direction to work towards and outline functionality. From the first example this would be a clear indicator to teams that they need to implement authentication and authorization. The last example means teams will need to create a guest feed and that data for that feed needs to be generally available.

### Adding Static Files

Static files in django include images and stylesheets. Django uses a specific syntax in order to grab and serve these static files.

Firstly inside `settings.py` you will need to make sure you have these two lines:

```python
INSTALLED_APPS = [
    ..., # installed apps
    'django.contrib.staticfiles',
    ... # other installed apps
]
```

```python
STATIC_URL = "static/"
```

This will only work while `DEBUG=True` in `settings.py`. Changing it to false will necessitate additional lines of code.

Once you've added these lines you'll be ready to serve your static files. Once you've made a new application (we'll call it `my_app` for now) you can create a directory called `static/my_app/` and add your files for it there. The reason we create the `my_app` subdirectory is for the purposes of namespacing.

Inside `static/my_app/` you can create a new `style.css` with some simple styling to test it:

```css
h1 {
    color: red;
}
```

Finally, in the `<head>` for `base.html` link the stylesheet using Django's static path:

```html
{% load static %}
<link rel="stylesheet" href="{% static 'my_app/style.css' %}">
```

## Exercises

Today you'll be creating a mini-project. Follow the deliverables below:

- Ideate and present your user stories based on the other deliverables
- Create a django project and application on a topic of your choice
- Create a `base.html`
- Create a stylesheet and link it as a static file to your `base.html` 
- Create 3 html templates with corresponding views and url paths
- Create a navbar in the `base.html` in order to get to each of your pages
- Download any number of images and use them as static files in at least one of your html pages

Things not to include:

- Do not include any user interactions such as button clicks or form submissions
- Assume all users are guests and have full access to the site without login and user privileges

In order to get started on your mini-project please reference yesterday's content.

## BONUS: Embedding Youtube Content

Go to http://youtube.com and find a video to your liking. Note that some videos cannot be embedded and you generally won't know until you attempt to embed it.

Under the `Share` option choose `Embed` and copy paste the iframe into one of your views. It will look something like this:

```html
<iframe width="560" height="315" src="https://www.youtube.com/embed/ABCD1234" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
```

The video should now appear whenever you render that view. An important thing to notice about the youtube video is each video has an id. Inside the url for the embed (for example: `https://www.youtube.com/embed/ABCD1234`) you will be able to find that particular id (for example: `ABCD1234`).

We can set up our player to dynamically render a video or videos:

```python
def render_favorite_videos(request):
    context = {
        fav_videos: [
            'ABCD1234',
            'EFGH5678',
            'IJKL9012'
        ]
    }
    return render(request, 'app_name/youtube_videos.html', context)
```

And inside the template:

```html
{% for video_id in fav_videos %}

<iframe width="560" height="315" src="https://www.youtube.com/embed/{{ video_id }}" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

{% endfor %}
```

Notice where we've used the variable tags inside the loop.