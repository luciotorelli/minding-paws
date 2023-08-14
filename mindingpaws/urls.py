from . import views
from django.urls import path
from allauth.account.views import PasswordChangeView

urlpatterns = [
    path('', views.HomeRedirectView.as_view(), name='home'),
    path('welcome/', views.WelcomeView.as_view(), name='welcome'),
    path('pet-owner-signup/', views.PetOwnerSignUp.as_view(), name='pet-owner-signup'),
    path('minder-signup/', views.MinderSignUp.as_view(), name='minder-signup'),
    path('create-booking/', views.CreateBookingView.as_view(), name='create-booking'),
    path('browse-minders/', views.BrowseMindersView.as_view(), name='browse-minders'),
    path('bookings/', views.BookingsView.as_view(), name='bookings'),
    path('update-booking-status/', views.UpdateBookingStatus.as_view(), name='update-booking-status'),
    path('edit-booking-details/', views.EditBookingDetailsView.as_view(), name='edit-booking-details'),
    path('my-profile-minder/', views.UpdateMinderView.as_view(), name='my-profile-minder'),
    path('my-profile-pet-owner/', views.UpdatePetOwnerView.as_view(), name='my-profile-pet-owner'),
    path('my-profile-redirect/', views.ProfileRedirectView.as_view(), name='my-profile-redirect'),
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),
    path('about-us/', views.AboutUsView.as_view(), name='about-us'),
]