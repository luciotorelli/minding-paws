from . import views
from django.urls import path

urlpatterns = [
    path('', views.HomeRedirectView.as_view(), name='home'),
    path('welcome/', views.welcomeView.as_view(), name='welcome'),
    path('pet-owner-signup/', views.PetOwnerSignUp.as_view(), name='pet-owner-sign-up'),
    path('minder-signup/', views.MinderSignUp.as_view(), name='minder-sign-up'),
    path('create-booking/', views.CreateBookingView.as_view(), name='create-booking'),
    path('browse-minders/', views.BrowseMindersView.as_view(), name='browse-minders'),
    path('bookings/', views.BookingsView.as_view(), name='bookings'),
]