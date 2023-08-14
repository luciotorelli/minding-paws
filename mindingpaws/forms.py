from django import forms
from .models import Minder, User, Booking
from allauth.account.forms import SignupForm
from cloudinary.forms import CloudinaryFileField
from django.forms import PasswordInput


class PetOwnerCreationForm(SignupForm):
    """
    Form for creating a Pet Owner user.

    This form extends the base SignupForm and adds fields specific to Pet Owners,
    such as name, role, pet_name, and pet_species. The form handles saving the user
    instance with the provided data.

    Fields:
        name (CharField): The full name of the Pet Owner.
        role (CharField): The role of the user (set as 'pet-owner').
        pet_name (CharField): The name of the pet owned by the Pet Owner.
        pet_species (CharField): The species of the pet owned by the Pet Owner.

    Methods:
        save(request): Saves the user instance with the provided data.

    """
    name = forms.CharField(label='Full Name')
    role = forms.CharField(label='Role')
    pet_name = forms.CharField(label='Pet Name')
    pet_species = forms.CharField(label='Pet Species')

    def save(self, request):
        """
        Save the user instance with the provided data.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            User: The saved user instance.
        """
        user = super(PetOwnerCreationForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.role = 'pet-owner'
        user.pet_name = self.cleaned_data['pet_name']
        user.pet_species = self.cleaned_data['pet_species']
        user.account_type = 1
        user.save()
        return user


class MinderCreationForm(SignupForm):
    """
    Form for creating a Minder user.

    This form extends the base SignupForm and adds fields specific to Minders,
    such as name, bio, usual_availability, and photo. The form handles saving
    the user instance and creating a corresponding Minder instance with the provided data.

    Fields:
        name (CharField): The name of the Minder.
        bio (CharField): The bio/description of the Minder.
        usual_availability (CharField): The usual availability of the Minder.
        photo (CloudinaryFileField): The photo of the Minder (optional).

    Methods:
        save(request): Saves the user instance and creates a corresponding Minder instance with the provided data.

    """
    name = forms.CharField(label='Name')
    bio = forms.CharField(label='Bio')
    usual_availability = forms.CharField(label='Usual Availability')
    photo = CloudinaryFileField(
        options={
            'folder': 'static/img/minders',
            'resource_type': 'image'
        },
        required=False
    )

    def save(self, request):
        """
        Save the user instance and create a corresponding Minder instance with the provided data.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            User: The saved user instance.
        """
        user = super().save(request)
        user.role = 'minder'
        user.account_type = 2
        user.name = self.cleaned_data['name']
        user.save()
        minder = Minder.objects.create(
            user=user,
            bio=self.cleaned_data['bio'],
            usual_availability=self.cleaned_data['usual_availability'],
            photo=self.cleaned_data['photo']
        )
        return user


class BookingCreationForm(forms.ModelForm):
    """
    Form for creating a booking.

    This form extends from ModelForm and is used to create a new booking instance.
    It includes fields for the Booking model along with predefined widgets and
    customized initialization and save methods.

    Fields:
        All fields from the Booking model.

    Widgets:
        Various widgets to customize the rendering of specific fields.

    Methods:
        __init__(*args, **kwargs): Redefines field values on initialization.
        save(commit=True): Saves the booking instance, setting the status to pending if new.

    """
    class Meta:
        model = Booking
        fields = '__all__'
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'pet_owner_name': forms.TextInput(attrs={'readonly': 'readonly'}),
            'bio': forms.TextInput(attrs={'readonly': 'readonly'}),
            'usual_availability': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Redefine values for fields on initialization.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.fields['pet_owner'].queryset = User.objects.filter(
            role='pet-owner')

        # Set the status value to pending
        self.fields['status'].initial = 'pending'

    def save(self, commit=True):
        """
        Save the booking instance.

        Set status to pending if it's being created for the first time, but allows
        it to be edited from the admin later on.

        Args:
            commit (bool, optional): If it should be saved to the data. Defaults to True.

        Returns:
            instance: The instance of the form/data opened.
        """
        instance = super().save(commit=False)
        if not instance.pk:  
            instance.status = 'pending'
        if commit:
            instance.save()
        return instance

    
class UpdateBookingStatusForm(forms.Form):
    """
    Form for updating booking status.

    This form is used to update the status of a booking. It includes fields for the
    booking_id and status, with appropriate data types and maximum lengths.

    Fields:
        booking_id (IntegerField): The ID of the booking.
        status (CharField): The updated status of the booking.

    """
    booking_id = forms.IntegerField()
    status = forms.CharField(max_length=10)


class EditBookingDetailsForm(forms.Form):
    """
    Form for editing booking details.

    This form is used to edit the details of a booking. It includes fields for the
    booking_id, pet_name, pet_species, and service_description.

    Fields:
        booking_id (IntegerField): The ID of the booking (hidden input).
        pet_name (CharField): The name of the pet for the booking.
        pet_species (CharField): The species of the pet for the booking.
        service_description (CharField): The description of the service for the booking.

    """
    booking_id = forms.IntegerField(widget=forms.HiddenInput())
    pet_name = forms.CharField(max_length=100, label='Pet Name')
    pet_species = forms.CharField(max_length=100, label='Pet Species')
    service_description = forms.CharField(widget=forms.Textarea, label='Service Description')


class UpdateMinderForm(forms.ModelForm):
    """
    Form for updating a Minder's profile.

    This form is used to update a Minder's profile information, including fields such
    as bio, usual_availability, and photo. Additionally, the form allows changing the
    name, email, and password of the Minder.

    Fields:
        bio (CharField): The bio/description of the Minder.
        usual_availability (CharField): The usual availability of the Minder.
        photo (CloudinaryFileField): The photo of the Minder.
        name (CharField): The name of the Minder.
        email (EmailField): The email of the Minder.
        password1 (CharField): The new password for the Minder (optional).
        password2 (CharField): The confirmation of the new password (optional).

    Methods:
        __init__(*args, **kwargs): Customize widget attributes and help text on initialization.
        clean(): Validate password fields and check for matching passwords.

    """
    class Meta:
        model = Minder
        fields = ['bio', 'usual_availability', 'photo']

    name = forms.CharField(label='Name')
    email = forms.EmailField(label='Email')
    password1 = forms.CharField(
        widget=PasswordInput(render_value=True),
        required=False, 
        label='Password'
    )
    password2 = forms.CharField(
        widget=PasswordInput(render_value=True),
        required=False,
        label='Confirm Password'
    )

    def __init__(self, *args, **kwargs):
        """
        Customize widget attributes and help text on initialization.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['value'] = ''
        self.fields['password2'].widget.attrs['value'] = ''
        self.fields['password1'].help_text = "Leave this field blank to keep the current password."
        self.fields['password2'].help_text = "Leave this field blank to keep the current password."

    def clean(self):
        """
        Validate password fields and check for matching passwords.

        Returns:
            dict: Cleaned data after validation.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
       
        if password1 and not password2:
            self.add_error('password2', forms.ValidationError("This field must be filled if Password is entered."))

        if password2 and not password1:
            self.add_error('password1', forms.ValidationError("This field must be filled if Confirm Password is entered."))

        if password1 and password2 and password1 != password2:
            self.add_error('password1', forms.ValidationError("Passwords do not match."))
            self.add_error('password2', forms.ValidationError("Passwords do not match."))

        return cleaned_data

class UpdatePetOwnerForm(forms.ModelForm):
    """
    Form for updating a Pet Owner's profile.

    This form is used to update a Pet Owner's profile information, including fields such
    as name, email, pet_name, and pet_species. Additionally, the form allows changing the
    password of the Pet Owner.

    Fields:
        password1 (CharField): The new password for the Pet Owner (optional).
        password2 (CharField): The confirmation of the new password (optional).

    Meta:
        model (User): The User model that the form is based on.
        fields (list): The list of fields from the User model that should be included in the form.

    Methods:
        clean(): Validate password fields and check for matching passwords.

    """
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        required=False,
    )
    password2 = forms.CharField(
        label="Confirm Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        required=False,
    )

    class Meta:
        model = User
        fields = ['name', 'email', 'pet_name', 'pet_species']

    def clean(self):
        """
        Validate password fields and check for matching passwords.

        Returns:
            dict: Cleaned data after validation.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
       
        if password1 and not password2:
            self.add_error('password2', forms.ValidationError("This field must be filled if Password is entered."))

        if password2 and not password1:
            self.add_error('password1', forms.ValidationError("This field must be filled if Confirm Password is entered."))

        if password1 and password2 and password1 != password2:
            self.add_error('password1', forms.ValidationError("Passwords do not match."))
            self.add_error('password2', forms.ValidationError("Passwords do not match."))

        return cleaned_data
