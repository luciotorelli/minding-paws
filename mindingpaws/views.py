from django.views.generic import TemplateView, View
from django.views.generic.edit import FormView, UpdateView
from django.views.generic import ListView
from allauth.account.views import SignupView
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Q
from .forms import *
from .models import User, Minder, Booking
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.utils import timezone

class welcomeView(TemplateView):
    template_name = 'index.html'


class HomeRedirectView(View):
    # Redirect user to bookings if logged in, else, redirect user to welcome page.
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('bookings')
        else:
            return redirect('welcome')

class AboutUsView(TemplateView):
    template_name = 'about_us.html'

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
        messages.success(self.request, "Booking created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, "There was an issue with your form submission. Verify any displayed errors or contact us.")
        return super().form_invalid(form)


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
        """get_queryset

        Verify if the user is logged in and has a minder or a pet owner attached to it to filter the bookings.

        Returns:
            obj: The filtered objects
        """
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'minder'):
            return Booking.objects.filter(minder=user.minder)
        elif user.is_authenticated and user.role == 'pet-owner':
            return Booking.objects.filter(pet_owner=user)
        else:
            return Booking.objects.none()

    def update_completed_statuses(self, bookings):
        now = timezone.now()
        for booking in bookings:
            if booking.status == 'accepted' and booking.end_date < now:
                booking.status = 'completed'
                booking.save()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bookings = context['bookings']

        self.update_completed_statuses(bookings)

        context['pending_bookings'] = bookings.filter(status='pending')
        context['accepted_bookings'] = bookings.filter(status='accepted')
        context['cancelled_bookings'] = bookings.filter(status='cancelled')
        context['completed_bookings'] = bookings.filter(status='completed')
        return context
    
class UpdateBookingStatus(View):
    def post(self, request, *args, **kwargs):
        form = UpdateBookingStatusForm(request.POST)
        if form.is_valid():
            booking_id = form.cleaned_data['booking_id']
            status = form.cleaned_data['status']
            booking = get_object_or_404(Booking, id=booking_id)

            # If status is being set to accepted and user is not a minder, raise PermissionDenied
            if status == 'accepted' and request.user.role != 'minder':
                raise PermissionDenied("Only a minder can accept a booking.")

            # If status is being set to cancelled, ensure status is not cancelled or completed
            if status == 'cancelled' and (booking.status == 'cancelled' or booking.status == 'completed'):
                raise PermissionDenied("You can't cancel a booking that is already cancelled or completed.")
            
            # If status is being set to deleted, ensure status is completed
            if status == 'deleted':
                if booking.status != 'completed':
                    raise PermissionDenied("You can only delete completed bookings.")
                booking.delete()

            messages.success(self.request, "Booking status updated successfully!")

            booking.status = status
            booking.save()

        return redirect('bookings')

    def form_invalid(self, form):
        messages.warning(self.request, "There was an issue updating the booking status. Verify any displayed errors or contact us.")
        return super().form_invalid(form)

class EditBookingDetailsView(View):
    def post(self, request, *args, **kwargs):
        form = EditBookingDetailsForm(request.POST)
        if form.is_valid():
            booking_id = form.cleaned_data['booking_id']
            booking = get_object_or_404(Booking, id=booking_id)
            
            # Check if the booking status is 'pending' and the user role is 'pet-owner'
            if booking.status == 'pending' and request.user.role == 'pet-owner':
                booking.pet_name = form.cleaned_data['pet_name']
                booking.pet_species = form.cleaned_data['pet_species']
                booking.service_description = form.cleaned_data['service_description']
                booking.save()
                messages.success(self.request, "Booking details updated successfully!")
            else:
                messages.warning(self.request, "You are not authorized to edit this booking.")
        return redirect('bookings')

class UpdateMinderView(UpdateView):
    model = Minder
    template_name = 'my-profile-minder.html'
    form_class = UpdateMinderForm
    success_url = '/my-profile-minder/'

    def get_object(self, queryset=None):
        return self.request.user.minder  # Retrieve the logged-in user's Minder instance

    def get_initial(self):
        initial = super().get_initial()
        initial['name'] = self.request.user.name
        initial['email'] = self.request.user.email
        initial['photo'] = None  # Set the photo field to None to make it show as empty
        return initial

    def form_valid(self, form):
        # Save the Minder and User fields separately
        minder = form.save(commit=False)
        minder.bio = form.cleaned_data['bio']
        minder.usual_availability = form.cleaned_data['usual_availability']
        # Check if a new photo file is provided before saving
        new_photo = form.cleaned_data['photo']
        if new_photo:
            minder.photo = new_photo
        
        minder.save()

        user = self.request.user
        user.name = form.cleaned_data['name']
        user.email = form.cleaned_data['email']
        # Update password only if provided
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']
        if password1 and password2 and password1 == password2:
            user.set_password(password1)
            user.save()
            # Keep the user logged in after changing password
            update_session_auth_hash(self.request, user)
        user.save()

        messages.success(self.request, "Profile updated successfully!")

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update'
        return context

    def form_invalid(self, form):
        messages.warning(self.request, "There was an issue updating your profile. Verify any displayed errors or contact us.")
        return super().form_invalid(form)

class UpdatePetOwnerView(UpdateView):
    model = User
    template_name = 'my-profile-pet-owner.html'
    form_class = UpdatePetOwnerForm
    success_url = '/my-profile-pet-owner/'

    def get_object(self, queryset=None):
        return self.request.user  # Retrieve the logged-in user's pet owner instance

    def get_initial(self):
        initial = super().get_initial()
        initial['pet_name'] = self.request.user.pet_name
        initial['pet_species'] = self.request.user.pet_species
        return initial

    def form_valid(self, form):
        pet_owner = form.save(commit=False)
        pet_owner.pet_name = form.cleaned_data['pet_name']
        pet_owner.pet_species = form.cleaned_data['pet_species']
        
        # Update password if provided
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']
        if password1 and password2 and password1 == password2:
            pet_owner.set_password(password1)
            pet_owner.save()
            # Keep the user logged in after changing password
            update_session_auth_hash(self.request, pet_owner)
        
        pet_owner.save()

        messages.success(self.request, "Profile updated successfully!")

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update'
        return context

    def form_invalid(self, form):
        messages.warning(self.request, "There was an issue updating your profile. Verify any displayed errors or contact us.")
        return super().form_invalid(form)

class ProfileRedirectView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = request.user

            if user.role == 'pet-owner':
                return redirect('my-profile-pet-owner')
            elif hasattr(user, 'minder'):
                return redirect('my-profile-minder')
        else:
            # If the user is not authenticated, redirect to welcome page.
            return redirect('welcome')