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
        return render(request, 'coffee_app/beverage_create.html', context)

    # POST #
    # this is the same as the `if method == 'POST'` from functional views
    def post(self, request):
        form = BeverageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            context = { "form": form }
            return render(request, 'coffee_app/beverage_create.html', context)
        

from django.views.generic.edit import FormView

# FormView is a more specialized view that handles form submissions
class AlternateBeverageCreateView(FormView):
    # template to render
    template_name = 'coffee_app/beverage_create.html'
    # form we're using
    form_class = BeverageForm
    # where we go when the form is submitted correctly
    success_url = '/'

    # what happens when the form is valid
    def form_valid(self, form):
        form.save() # save the form
        return super().form_valid(form) 
        # trigger the FormView's form_valid method



from django.views.generic import ListView
from .models import Beverage

# ListView will render a list page and automatically 
# pass all the items for a model
class BeverageListView(ListView):
    model = Beverage
    context_object_name = 'all_beverages'


# CONVENTION vs CONFIGURATION

# convention -- shortcuts we can use to make coding easier
# BUT those shortcuts make it harder to do custom logic
# and configure things in a more precise

# configuration -- we do a lot of the logic and heavy lifting
# BUT we can customize more readily


from django.views.generic import DetailView

# DetailView will take in a pk and show a page for just that item
class BeverageDetailView(DetailView):
    model = Beverage
    context_object_name = 'beverage'