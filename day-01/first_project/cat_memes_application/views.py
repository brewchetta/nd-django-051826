from django.shortcuts import render

# the view will process the request and then render a template
# http://127.0.0.1:8000
def homepage(request):
    return render(request, "cat_memes_application/homepage.html")

def login(request):
    return render(request, "cat_memes_application/login.html")

def memes(request):
    cat_meme_urls = [
        "https://upload.wikimedia.org/wikipedia/commons/d/dc/Grumpy_Cat_%2814556024763%29_%28cropped%29.jpg?utm_source=en.wikipedia.org&utm_campaign=index&utm_content=original",

        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ2v1HCs4g7fqBJMaobrYD80zJi5yx8vVNg6g&s",

        "https://upload.wikimedia.org/wikipedia/en/1/1f/WomanYellingAtACat_meme.jpg",
    ]

    # context is used to pass information to the template
    # it is a dictionary (key / value pairs)
    context = {
        "urls": cat_meme_urls,
        "num_memes": len( cat_meme_urls ),
        "something_else": "I am something else"
    }

    return render(request, "cat_memes_application/memes.html", context)
    # context is the final optional argument in render

# with dynamic url (int:num_one, int:num_two)
def addition(request, num_one, num_two):
    context = {
        "num_one": num_one,
        "num_two": num_two,
        "final_result": num_one + num_two
    }

    return render(request, "cat_memes_application/addition.html", context)