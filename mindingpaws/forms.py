from django import forms
from .models import Minder, User, Booking
from allauth.account.forms import SignupForm
from cloudinary.forms import CloudinaryFileField


class PetOwnerCreationForm(SignupForm):
    name = forms.CharField(label='Full Name')
    role = forms.CharField(label='Role')
    pet_name = forms.CharField(label='Pet Name')
    pet_species = forms.CharField(label='Pet Species')

    def save(self, request):
        user = super(PetOwnerCreationForm, self).save(request)
        user.name = self.cleaned_data['name']
        user.role = 'pet-owner'
        user.pet_name = self.cleaned_data['pet_name']
        user.pet_species = self.cleaned_data['pet_species']
        user.account_type = 1
        user.save()
        return user


class MinderCreationForm(SignupForm):
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
        """__init__ 

        Redefine values for fields on initialization
        """
        super().__init__(*args, **kwargs)
        self.fields['pet_owner'].queryset = User.objects.filter(
            role='pet-owner')

        # Set the status value to pending
        self.fields['status'].initial = 'pending'

    def save(self, commit=True):
        """save

        Set status to pending if it's being created for the first time, but allows it to be edited from the admin later on.

        Args:
            commit (bool, optional): If it should be saved to the data. Defaults to True.

        Returns:
            instance: The instance of the form/data opened
        """
        instance = super().save(commit=False)
        if not instance.pk:  
            instance.status = 'pending'
        if commit:
            instance.save()
        return instance
    
class UpdateBookingStatusForm(forms.Form):
    booking_id = forms.IntegerField()
    status = forms.CharField(max_length=10)