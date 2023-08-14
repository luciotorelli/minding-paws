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

class WelcomeView(TemplateView):
    """
    A view that displays the welcome page using the 'index.html' template.
    """
    template_name = 'index.html'


class HomeRedirectView(View):
    """
    A view that redirects users based on their authentication status.

    If the user is logged in, they are redirected to the 'bookings' page.
    If the user is not logged in, they are redirected to the 'welcome' page.
    """
    def get(self, request, *args, **kwargs):
        """
        Handles the HTTP GET request for redirection.

        Args:
            request: The HTTP request object.

        Returns:
            HTTPResponse: A redirection response based on the user's authentication status.
        """
        if request.user.is_authenticated:
            return redirect('bookings')
        else:
            return redirect('welcome')

class AboutUsView(TemplateView):
    """
    A view that displays the 'about us' page using the 'about_us.html' template.
    """
    template_name = 'about_us.html'

class PetOwnerSignUp(SignupView):
    """
    A view for signing up as a pet owner.

    This view displays the 'signup_pet_owner.html' template for pet owner registration.
    After successful registration, users are redirected to the home page.
    """
    template_name = 'account/signup_pet_owner.html'
    form_class = PetOwnerCreationForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        """
        Retrieves and prepares additional context data for the template.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Context data to be passed to the template.
        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Pet Owner Sign Up'
        return context


class MinderSignUp(SignupView):
    """
    View for handling Minder sign-up.

    This view handles the sign-up process for Minders, using the provided
    template and form class for rendering and processing the form. Upon
    successful sign-up, the user is redirected to the home page.

    Attributes:
        template_name (str): The name of the template for rendering the sign-up page.
        form_class (class): The form class used for Minder sign-up.
        success_url (str): The URL to redirect to upon successful sign-up.

    Methods:
        get_context_data(**kwargs): Retrieves and adds 'title' to the context data.

    """
    template_name = 'account/signup_minder.html'
    form_class = MinderCreationForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        """
        Retrieve context data for rendering the sign-up page.

        This method overrides the parent class's method to add the 'title'
        to the context data. The 'title' is set to 'Minder Sign Up'.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: Context data containing 'title' for rendering the page.

        """
        context = super().get_context_data(**kwargs)
        context['title'] = 'Minder Sign Up'
        return context


class CreateBookingView(LoginRequiredMixin, FormView):
    """
    View for creating a booking.

    This view handles the creation of a booking using the provided form.
    The view requires the user to be logged in and uses the specified
    template for rendering the booking creation page. Upon successful
    booking creation, the user is redirected to the home page.

    Attributes:
        template_name (str): The name of the template for rendering the booking creation page.
        form_class (class): The form class used for booking creation.
        success_url (str): The URL to redirect to upon successful booking creation.

    Methods:
        get_initial(): Retrieves and returns initial form data based on the logged-in user.
        clean(): Validates form data to prevent changing default values of logged-in pet_owner and pet_owner_name.
        form_valid(form): Saves the booking form and displays a success message.
        form_invalid(form): Displays a warning message for form submission issues.

    """

    template_name = 'create_booking.html'
    form_class = BookingCreationForm
    success_url = ('/')

    def get_initial(self):
        """
        Get initial form data based on the logged-in user.

        Returns:
            dict: Initial form data including pet owner details from the logged-in user.
        """
        initial = super().get_initial()
        user = self.request.user
        initial['pet_owner'] = user.pk
        initial['pet_owner_name'] = user.name
        initial['pet_name'] = user.pet_name
        initial['pet_species'] = user.pet_species
        return initial

    def clean(self):
        """
        Validate form data to prevent changing default pet_owner and pet_owner_name values.

        Raises:
            ValidationError: If pet owner details are different from the logged-in user.
        """
        cleaned_data = super().clean()
        initial_pet_owner = self.initial.get('pet_owner')
        initial_pet_owner_name = self.initial.get('pet_owner_name')

        pet_owner = cleaned_data.get('pet_owner')
        pet_owner_name = cleaned_data.get('pet_owner_name')

        if pet_owner != initial_pet_owner or pet_owner_name != initial_pet_owner_name:
            raise ValidationError({
                'pet_owner_name': "Pet owner name cannot be different from logged-in user.",
                'pet_owner': "Pet owner cannot be different from logged-in user."
            })

    def form_valid(self, form):
        """
        Save the booking form and display a success message.

        Args:
            form: The validated form.

        Returns:
            HttpResponse: A response indicating successful form submission.
        """
        form.save()
        messages.success(self.request, "Booking created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        """
        Display a warning message for form submission issues.

        Args:
            form: The form with submission issues.

        Returns:
            HttpResponse: A response indicating form submission issues.
        """
        messages.warning(self.request, "There was an issue with your form submission. Verify any displayed errors or contact us.")
        return super().form_invalid(form)


class BrowseMindersView(ListView):
    """
    View for browsing and searching minders.

    This view lists and filters minders based on search criteria provided by users.
    The view uses the specified template for rendering and provides context for
    pagination.

    Attributes:
        model (class): The model class for the minder.
        template_name (str): The name of the template for rendering the browse minders page.
        context_object_name (str): The name to be used for the queryset in the template's context.
        paginate_by (int): The number of minders to display per page.

    Methods:
        get_queryset(): Retrieves the queryset of minders based on search criteria.
        get_context_data(**kwargs): Retrieves context data for the view, including an 'is_ajax' flag.
        render_to_response(context, **response_kwargs): Renders the appropriate response based on AJAX requests.

    """
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
    """
    View for displaying bookings.

    This view displays bookings based on the user's role (minder or pet owner) and their logged-in status.
    Bookings are categorized into pending, accepted, cancelled, and completed.

    Attributes:
        template_name (str): The name of the template for rendering the bookings page.
        context_object_name (str): The name to be used for the queryset in the template's context.

    Methods:
        get_queryset(): Retrieves the queryset of bookings based on user's role and logged-in status.
        update_completed_statuses(bookings): Updates booking statuses to 'completed' if they have ended.
        get_context_data(**kwargs): Retrieves context data for the view, including categorized bookings.

    """
    template_name = 'bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        """
        Get the queryset of bookings based on user's role and logged-in status.

        Returns:
            QuerySet: The filtered bookings queryset based on user's role and logged-in status.
        """
        user = self.request.user
        if user.is_authenticated and hasattr(user, 'minder'):
            return Booking.objects.filter(minder=user.minder)
        elif user.is_authenticated and user.role == 'pet-owner':
            return Booking.objects.filter(pet_owner=user)
        else:
            return Booking.objects.none()

    def update_completed_statuses(self, bookings):
        """
        Update booking statuses to 'completed' if they have ended.

        Args:
            bookings (QuerySet): The queryset of bookings.

        Returns:
            None
        """
        now = timezone.now()
        for booking in bookings:
            if booking.status == 'accepted' and booking.end_date < now:
                booking.status = 'completed'
                booking.save()

    def get_context_data(self, **kwargs):
        """
        Get the context data for the view.

        Updates booking statuses, categorizes bookings, and adds categorized bookings to context.

        Returns:
            dict: The context data for the view.
        """
        context = super().get_context_data(**kwargs)
        bookings = context['bookings']

        self.update_completed_statuses(bookings)

        context['pending_bookings'] = bookings.filter(status='pending')
        context['accepted_bookings'] = bookings.filter(status='accepted')
        context['cancelled_bookings'] = bookings.filter(status='cancelled')
        context['completed_bookings'] = bookings.filter(status='completed')
        return context
    
class UpdateBookingStatus(View):
    """
    View for updating booking status.

    This view handles the updating of booking status based on the provided form data.
    It verifies the user's role and booking status, and performs corresponding actions
    such as accepting, cancelling, or deleting a booking.

    Methods:
        post(request, *args, **kwargs): Handles the POST request to update the booking status.
        form_invalid(form): Handles the case of an invalid form submission.

    """

    def post(self, request, *args, **kwargs):
        """
        Handle the POST request to update the booking status.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: A redirect response after updating the booking status.
        """
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
        """
        Handle the case of an invalid form submission.

        Args:
            form: The form with submission issues.

        Returns:
            HttpResponse: A response indicating form submission issues.
        """
        messages.warning(self.request, "There was an issue updating the booking status. Verify any displayed errors or contact us.")
        return super().form_invalid(form)


class EditBookingDetailsView(View):
    """
    View for editing booking details.

    This view handles the editing of booking details based on the provided form data.
    It verifies the user's role and booking status before allowing editing.

    Methods:
        post(request, *args, **kwargs): Handles the POST request to edit booking details.

    """

    def post(self, request, *args, **kwargs):
        """
        Handle the POST request to edit booking details.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: A redirect response after editing booking details.
        """
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
    """
    View for updating Minder profile.

    This view allows Minders to update their profile information, including name, email,
    photo, bio, usual_availability, and password. It uses a form for updating the fields.

    Attributes:
        model (class): The model class for the Minder.
        template_name (str): The name of the template for rendering the Minder profile update page.
        form_class (class): The form class used for updating Minder profile.
        success_url (str): The URL to redirect to upon successful profile update.

    Methods:
        get_object(queryset=None): Retrieves the Minder instance of the logged-in user.
        get_initial(): Retrieves initial form data based on the logged-in user's information.
        form_valid(form): Saves the Minder and User fields after validating the form.
        get_context_data(**kwargs): Retrieves context data for the view.
        form_invalid(form): Handles the case of an invalid form submission.

    """
    model = Minder
    template_name = 'my-profile-minder.html'
    form_class = UpdateMinderForm
    success_url = '/my-profile-minder/'

    def get_object(self, queryset=None):
        """
        Retrieve the Minder instance of the logged-in user.

        Args:
            queryset: The queryset to retrieve the object from.

        Returns:
            Minder: The Minder instance of the logged-in user.
        """
        return self.request.user.minder  # Retrieve the logged-in user's Minder instance

    def get_initial(self):
        """
        Retrieve initial form data based on the logged-in user's information.

        Returns:
            dict: Initial form data for updating Minder profile.
        """
        initial = super().get_initial()
        initial['name'] = self.request.user.name
        initial['email'] = self.request.user.email
        initial['photo'] = None  # Set the photo field to None to make it show as empty
        return initial

    def form_valid(self, form):
        """
        Save the Minder and User fields after validating the form.

        Args:
            form: The validated form.

        Returns:
            HttpResponse: A response indicating successful profile update.
        """
        minder = form.save(commit=False)
        minder.bio = form.cleaned_data['bio']
        minder.usual_availability = form.cleaned_data['usual_availability']
        new_photo = form.cleaned_data['photo']
        if new_photo:
            minder.photo = new_photo
        
        minder.save()

        user = self.request.user
        user.name = form.cleaned_data['name']
        user.email = form.cleaned_data['email']
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']
        if password1 and password2 and password1 == password2:
            user.set_password(password1)
            user.save()
            update_session_auth_hash(self.request, user)
        user.save()

        messages.success(self.request, "Profile updated successfully!")

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Retrieve context data for the view.

        Returns:
            dict: Context data for the view.
        """
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update'
        return context

    def form_invalid(self, form):
        """
        Handle the case of an invalid form submission.

        Args:
            form: The form with submission issues.

        Returns:
            HttpResponse: A response indicating form submission issues.
        """
        messages.warning(self.request, "There was an issue updating your profile. Verify any displayed errors or contact us.")
        return super().form_invalid(form)


class UpdatePetOwnerView(UpdateView):
    """
    View for updating Pet Owner profile.

    This view allows Pet Owners to update their profile information, including pet_name,
    pet_species, and password. It uses a form for updating the fields.

    Attributes:
        model (class): The model class for the User.
        template_name (str): The name of the template for rendering the Pet Owner profile update page.
        form_class (class): The form class used for updating Pet Owner profile.
        success_url (str): The URL to redirect to upon successful profile update.

    Methods:
        get_object(queryset=None): Retrieves the User instance of the logged-in user.
        get_initial(): Retrieves initial form data based on the logged-in user's pet information.
        form_valid(form): Saves the User fields after validating the form.
        get_context_data(**kwargs): Retrieves context data for the view.
        form_invalid(form): Handles the case of an invalid form submission.

    """
    model = User
    template_name = 'my-profile-pet-owner.html'
    form_class = UpdatePetOwnerForm
    success_url = '/my-profile-pet-owner/'

    def get_object(self, queryset=None):
        """
        Retrieve the User instance of the logged-in user.

        Args:
            queryset: The queryset to retrieve the object from.

        Returns:
            User: The User instance of the logged-in user.
        """
        return self.request.user  # Retrieve the logged-in user's pet owner instance

    def get_initial(self):
        """
        Retrieve initial form data based on the logged-in user's pet information.

        Returns:
            dict: Initial form data for updating Pet Owner profile.
        """
        initial = super().get_initial()
        initial['pet_name'] = self.request.user.pet_name
        initial['pet_species'] = self.request.user.pet_species
        return initial

    def form_valid(self, form):
        """
        Save the User fields after validating the form.

        Args:
            form: The validated form.

        Returns:
            HttpResponse: A response indicating successful profile update.
        """
        pet_owner = form.save(commit=False)
        pet_owner.pet_name = form.cleaned_data['pet_name']
        pet_owner.pet_species = form.cleaned_data['pet_species']
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']
        if password1 and password2 and password1 == password2:
            pet_owner.set_password(password1)
            pet_owner.save()
            update_session_auth_hash(self.request, pet_owner)
        
        pet_owner.save()

        messages.success(self.request, "Profile updated successfully!")

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        """
        Retrieve context data for the view.

        Returns:
            dict: Context data for the view.
        """
        context = super().get_context_data(**kwargs)
        context['action'] = 'Update'
        return context

    def form_invalid(self, form):
        """
        Handle the case of an invalid form submission.

        Args:
            form: The form with submission issues.

        Returns:
            HttpResponse: A response indicating form submission issues.
        """
        messages.warning(self.request, "There was an issue updating your profile. Verify any displayed errors or contact us.")
        return super().form_invalid(form)


class ProfileRedirectView(View):
    """
    View for redirecting users to their respective profiles.

    This view checks the user's authentication status and role, and redirects them to
    their respective profile pages (Pet Owner or Minder). If the user is not authenticated,
    they are redirected to the welcome page.

    Methods:
        get(request, *args, **kwargs): Handles the GET request for redirecting users.
    """
    def get(self, request, *args, **kwargs):
        """
        Handle the GET request for redirecting users.

        Args:
            request (HttpRequest): The HTTP request object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            HttpResponse: A redirect response to the user's respective profile page or welcome page.
        """
        if request.user.is_authenticated:
            user = request.user

            if user.role == 'pet-owner':
                return redirect('my-profile-pet-owner')
            elif hasattr(user, 'minder'):
                return redirect('my-profile-minder')
        else:
            # If the user is not authenticated, redirect to welcome page.
            return redirect('welcome')
