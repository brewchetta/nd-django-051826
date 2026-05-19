from django.shortcuts import render

def homepage(request):
    return render(request, 'movie_app/homepage.html')

def upcoming_movies(request):
    movies_list = [
        {
            "title": "Supergirl", 
            "poster": "https://i.redd.it/7wgdxs5kqe6g1.jpeg", 
            "description": "Supergirl beats up some bad dudes."
        },
        {
            "title": "Disclosure Day",
            "poster": "https://m.media-amazon.com/images/M/MV5BMTgwNDI1ZjctYWNmMS00MTJhLTg1ZWItMzI1Yjk5NjZkYWFkXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
            "description": "Spielberg makes a movie about disclosing things about UFOs & extraterrestrials."
        }
    ]
    context = { "movies_list": movies_list }
    return render(request, 'movie_app/upcoming_movies.html', context)