from django import forms
from .models import Minder, User, Booking
from allauth.account.forms import SignupForm
from cloudinary.forms import CloudinaryFileField
from django.forms import PasswordInput


class PetOwnerCreationForm(SignupForm):
    """
    Form for creating a Pet Owner user.

    Extends the base SignupForm, adds fields specific
    to Pet Owners, like name, role, pet_name, pet_species.
    Saves user instance with provided data.

    Fields:
        name, role, pet_name, pet_species (CharField).

    Methods:
        save(request): Saves user with provided data.
    """
    name = forms.CharField(label='Full Name')
    role = forms.CharField(label='Role')
    pet_name = forms.CharField(label='Pet Name')
    pet_species = forms.CharField(label='Pet Species')

    def save(self, request):
        """
        Save user instance with provided data.

        Args:
            request (HttpRequest): HTTP request object.

        Returns:
            User: Saved user instance.
        """
        user = super().save(request)
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

    Extends SignupForm, adds fields for Minders,
    like name, bio, usual_availability, photo.
    Saves user and creates Minder with provided data.

    Fields:
        name, bio, usual_availability (CharField),
        photo (CloudinaryFileField).

    Methods:
        save(request): Saves user, creates Minder.
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
        Save user, create corresponding Minder with provided data.

        Args:
            request (HttpRequest): HTTP request object.

        Returns:
            User: Saved user instance.
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

    Extends ModelForm for new booking instance.
    Includes fields, widgets, custom initialization,
    and save methods.

    Fields:
        All fields from Booking model.

    Widgets:
        Various widgets for specific fields.

    Methods:
        __init__, save(commit=True).
    """
    class Meta:
        model = Booking
        fields = '__all__'
        widgets = {
            'start_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}),
            'pet_owner_name': forms.TextInput(
                attrs={'readonly': 'readonly'}),
            'bio': forms.TextInput(
                attrs={'readonly': 'readonly'}),
            'usual_availability': forms.TextInput(
                attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        """
        Redefine values for fields on initialization.

        Args:
            *args, **kwargs: Variable arguments.
        """
        super().__init__(*args, **kwargs)
        self.fields['pet_owner'].queryset = User.objects.filter(
            role='pet-owner')
        self.fields['status'].initial = 'pending'

    def save(self, commit=True):
        """
        Save booking instance.

        Sets status to pending if new, editable later.

        Args:
            commit (bool, optional): Defaults to True.

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

    Includes fields for booking_id and status.

    Fields:
        booking_id (IntegerField): ID of booking.
        status (CharField): Updated status of booking.
    """
    booking_id = forms.IntegerField()
    status = forms.CharField(max_length=10)


class EditBookingDetailsForm(forms.Form):
    """
    Form for editing booking details.

    Includes fields for booking_id, pet_name, pet_species,
    and service_description.

    Fields:
        booking_id (IntegerField): ID of booking (hidden).
        pet_name, pet_species (CharField): Pet details.
        service_description (CharField): Service details.
    """
    booking_id = forms.IntegerField(widget=forms.HiddenInput())
    pet_name = forms.CharField(max_length=100, label='Pet Name')
    pet_species = forms.CharField(max_length=100, label='Pet Species')
    service_description = forms.CharField(
        widget=forms.Textarea, label='Service Description')


class UpdateMinderForm(forms.ModelForm):
    """
    Form for updating a Minder's profile.

    Update Minder's profile, including bio, usual_availability,
    photo, name, email, password.

    Fields:
        bio, usual_availability (CharField),
        photo (CloudinaryFileField), name, email,
        password1, password2 (CharField).

    Methods:
        __init__, clean.
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
        Customize widget attributes, help text on initialization.

        Args:
            *args, **kwargs: Variable arguments.
        """
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs['value'] = ''
        self.fields['password2'].widget.attrs['value'] = ''
        self.fields['password1'].help_text = (
            "Leave this field blank to keep the current password.")
        self.fields['password2'].help_text = (
            "Leave this field blank to keep the current password.")

    def clean(self):
        """
        Validate password fields, check for matching passwords.

        Returns:
            dict: Cleaned data after validation.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and not password2:
            self.add_error('password2', forms.ValidationError(
                "This field must be filled if Password is entered."))
        if password2 and not password1:
            self.add_error('password1', forms.ValidationError(
                "This field must be filled if Confirm Password is entered."))
        if password1 and password2 and password1 != password2:
            self.add_error(
                'password1',
                forms.ValidationError("Passwords do not match."))
            self.add_error(
                'password2',
                forms.ValidationError("Passwords do not match."))

        return cleaned_data


class UpdatePetOwnerForm(forms.ModelForm):
    """
    Form for updating a Pet Owner's profile.

    Update Pet Owner's profile, including name, email,
    pet_name, pet_species, password.

    Fields:
        password1, password2 (CharField),
        model fields: name, email, pet_name, pet_species.

    Methods:
        clean.
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
        Validate password fields, check for matching passwords.

        Returns:
            dict: Cleaned data after validation.
        """
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and not password2:
            self.add_error('password2', forms.ValidationError(
                "This field must be filled if Password is entered."))

        if password2 and not password1:
            self.add_error('password1', forms.ValidationError(
                "This field must be filled if Confirm Password is entered."))

        if password1 and password2 and password1 != password2:
            self.add_error(
                'password1',
                forms.ValidationError("Passwords do not match."))
            self.add_error(
                'password2',
                forms.ValidationError("Passwords do not match."))

        return cleaned_data
