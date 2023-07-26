from . import views
from django.urls import path

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('pet-owner-signup/', views.PetOwnerSignUp.as_view(), name='pet-owner-sign-up'),
]