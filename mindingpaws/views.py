from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic import ListView
from allauth.account.views import SignupView
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Q
from .forms import PetOwnerCreationForm, MinderCreationForm, BookingCreationForm
from .models import Minder, Booking
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
                'pet_owner': "Pet owner cannot be different from logged in user."
            })

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class BrowseMindersView(ListView):
    model = Minder
    template_name = 'browse_minders.html'
    context_object_name = 'minders'
    paginate_by = 10

    def get_queryset(self):
        """
        Get the queryset of minders based on the search.

        Filters the minders based on a search for 'user__name' (from user attached to minder) and 'bio' fields.

        Returns:
            QuerySet: A result of minders based on the search.
        """
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(
                Q(user__name__icontains=query) | Q(bio__icontains=query))

        return queryset

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view.

        Adds a variable 'is_ajax' to the context data. It checks if the request is an AJAX request based on the
        'x-requested-with' header.

        Returns:
            dict: The context data for the view.
        """
        context = super().get_context_data(**kwargs)
        context['is_ajax'] = self.request.headers.get(
            "x-requested-with") == "XMLHttpRequest"
        return context

    def render_to_response(self, context, **response_kwargs):
        """
        Render the response.

        If the request is an AJAX request, renders the 'minders-results-partial.html' template and returns a JsonResponse
        containing the rendered HTML content. Otherwise, renders the full 'browse_minders.html' template.

        Args:
            context (dict): The context data for the view.
            response_kwargs (dict): Additional keyword arguments for the response.

        Returns:
            HttpResponse: The http response for the view.
        """
        if context['is_ajax']:
            html = render_to_string(
                template_name="minders-results-partial.html",
                context=context
            )
            data_dict = {"html_from_view": html}
            return JsonResponse(data=data_dict, safe=False)
        else:
            return super().render_to_response(context, **response_kwargs)


class BookingsView(LoginRequiredMixin, ListView):
    template_name = 'bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        user = self.request.user
        return Booking.objects.filter(pet_owner=user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bookings = context['bookings']
        context['pending_bookings'] = bookings.filter(status='pending')
        context['accepted_bookings'] = bookings.filter(status='accepted')
        context['cancelled_bookings'] = bookings.filter(status='cancelled')
        context['completed_bookings'] = bookings.filter(status='completed')
        return context
