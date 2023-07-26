from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from allauth.account.views import SignupView
from .forms import PetOwnerCreationForm

class HomeView(TemplateView):
    template_name = 'index.html'

class PetOwnerSignUp(SignupView):
    template_name = 'account/signup_pet_owner.html'
    form_class = PetOwnerCreationForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign Up'
        return context