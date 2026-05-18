from django.shortcuts import render

# the view will process the request and then render a template
# http://127.0.0.1:8000
def homepage(request):
    return render(request, "cat_memes_application/homepage.html")

def login(request):
    return render(request, "cat_memes_application/login.html")

def memes(request):
    return render(request, "cat_memes_application/memes.html")