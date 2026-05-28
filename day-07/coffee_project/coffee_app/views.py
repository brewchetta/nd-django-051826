from django.shortcuts import render

# FUNCTIONAL VIEWS #
def home(request):
    return render(request, 'coffee_app/home.html')


# CLASS BASED VIEWS #

from django.views.generic import TemplateView


# classes like to use upper camel case
class AboutView(TemplateView):
    template_name = 'coffee_app/about.html'


from datetime import datetime

# TemplateView is a specific view we're inheriting
class ClockView(TemplateView):
    extra_context = { "is_before_noon": datetime.now().hour < 12 }
    template_name = 'coffee_app/clock.html'


# extra context is basically just context, you can pass info to the view
class ContactView(TemplateView):
    extra_context = { 
        'contact_email': 'morning.bevs@bevs.com', 
        'contact_phone': '123-456-7890'
    }
    template_name = 'coffee_app/contact.html'


from django.views import View
from .forms import BeverageForm
from django.shortcuts import redirect

# the generic View is going to do something closer to a functional view
class BeverageCreateView(View):

    # GET #
    # this is the same as the get from the functional views
    def get(self, request):
        context = { "form": BeverageForm() }
        return render(request, 'coffee_app/greeting.html', context)

    # POST #
    # this is the same as the `if method == 'POST'` from functional views
    def post(self, request):
        form = BeverageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            context = { "form": form }
            return render(request, 'coffee_app/greeting.html', context)