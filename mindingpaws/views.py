from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from .forms import UserCreationForm

class HomeView(TemplateView):
    template_name = 'index.html'

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign Up'
        return context