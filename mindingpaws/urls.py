from . import views
from django.urls import path

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('pet-owner-signup/', views.PetOwnerSignUp.as_view(), name='pet-owner-sign-up'),
    path('minder-signup/', views.MinderSignUp.as_view(), name='minder-sign-up'),
    path('create-booking/', views.CreateBookingView.as_view(), name='create_booking'),
]