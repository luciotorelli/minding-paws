from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from allauth.account.views import SignupView
from .forms import PetOwnerCreationForm, MinderCreationForm, BookingCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin


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


class CreateBookingView(LoginRequiredMixin, FormView):
    template_name = 'create_booking.html'
    form_class = BookingCreationForm
    success_url = ('/')

    def get_initial(self):
        initial = super().get_initial()
        user = self.request.user
        initial['pet_owner'] = user.pk
        initial['pet_owner_name'] = user.name
        initial['pet_name'] = user.pet_name
        initial['pet_species'] = user.pet_species
        return initial

    # Clean to stop user from changing default values of logged-in pet_owner and pet_owner_name
    def clean(self):
        cleaned_data = super().clean()
        initial_pet_owner = self.initial.get('pet_owner')
        initial_pet_owner_name = self.initial.get('pet_owner_name')

        pet_owner = cleaned_data.get('pet_owner')
        pet_owner_name = cleaned_data.get('pet_owner_name')

        if pet_owner != initial_pet_owner or pet_owner_name != initial_pet_owner_name:
            raise ValidationError({
                'pet_owner_name': "Pet owner name cannot be different from logged in user.",
                'pet_owner':"Pet owner cannot be different from logged in user."
            })

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
