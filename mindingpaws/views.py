from django.views.generic import TemplateView
from allauth.account.views import SignupView
from .forms import PetOwnerCreationForm, MinderCreationForm

class HomeView(TemplateView):
    template_name = 'index.html'

class PetOwnerSignUp(SignupView):
    template_name = 'account/signup_pet_owner.html'
    form_class = PetOwnerCreationForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pet Owner Sign Up'
        return context

class MinderSignUp(SignupView):
    template_name = 'account/signup_minder.html'
    form_class = MinderCreationForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Minder Sign Up'
        return context