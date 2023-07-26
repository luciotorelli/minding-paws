from django import forms
from .models import Minder, User, Booking
from allauth.account.forms import SignupForm

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

    def save(self, request):
        user = super().save(request)
        user.role = 'minder'
        user.account_type = 2
        user.name = self.cleaned_data['name']
        user.save()
        minder = Minder.objects.create(
            user=user,
            bio=self.cleaned_data['bio'],
            usual_availability=self.cleaned_data['usual_availability']
        )
        return user

class BookingCreationForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """__init__ 

        Filter user field to only pick pet_owner_user with users role equal to pet owner when creating a Booking
        """
        super().__init__(*args, **kwargs)
        self.fields['pet_owner_user'].queryset = User.objects.filter(role='pet-owner')
