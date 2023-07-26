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
        user.role = self.cleaned_data['role']
        user.pet_name = self.cleaned_data['pet_name']
        user.pet_species = self.cleaned_data['pet_species']
        user.account_type = 1
        user.save()
        return user

class MinderCreationForm(forms.ModelForm):
    class Meta:
        model = Minder
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """__init__ 

        Filter user field to only pick users with role equal to minder when creating a Minder
        """
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(role='minder')

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
