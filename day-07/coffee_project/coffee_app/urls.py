from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # .as_view() is necessary for class based views
    path('about', views.AboutView.as_view(), name='about'),
    path('clock', views.ClockView.as_view(), name='clock'),
    path('contact', views.ContactView.as_view(), name='contact'),
    # path('beverages/create', views.BeverageCreateView.as_view(), name='beverage_create'),
    path('beverages/create', views.AlternateBeverageCreateView.as_view(), name='beverage_create'),
    path('beverages', views.BeverageListView.as_view(), name='beverage_list'),
    path('beverages/<int:pk>', views.BeverageDetailView.as_view(), name='beverage_detail')
]
