from django.shortcuts import render

def homepage(request):
    return render(request, 'second_app/homepage.html')

def subtraction(request, num_one, num_two):
    context = {
        "number_one": num_one,
        "number_two": num_two,
        "result": num_one - num_two
    }

    return render(request, "second_app/subtraction.html", context)