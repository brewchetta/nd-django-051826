from django.shortcuts import render

movies_list = [
    {
        "id": 0,
        "title": "Supergirl", 
        "poster": "https://i.redd.it/7wgdxs5kqe6g1.jpeg", 
        "description": "Supergirl beats up some bad dudes.",
        "youtube_id": "s1-pfiVMKAs?si=tK7r5XJv0ZLB6mX2"
    },
    {
        "id": 1,
        "title": "Disclosure Day",
        "poster": "https://m.media-amazon.com/images/M/MV5BMTgwNDI1ZjctYWNmMS00MTJhLTg1ZWItMzI1Yjk5NjZkYWFkXkEyXkFqcGc@._V1_FMjpg_UX1000_.jpg",
        "description": "Spielberg makes a movie about disclosing things about UFOs & extraterrestrials.",
        "youtube_id": "SCYT8vb2siQ?si=GdgV02U-PuKoxgP1"
    }
]

def homepage(request):
    return render(request, 'movie_app/homepage.html')

def upcoming_movies(request):
    context = { "movies_list": movies_list }
    return render(request, 'movie_app/upcoming_movies.html', context)

def trailer(request, movie_index):
    found_movie = movies_list[movie_index]
    context = {
        "title": found_movie["title"],
        "youtube_id": found_movie["youtube_id"]
    }

    return render(request, 'movie_app/trailer.html', context)