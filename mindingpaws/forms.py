from django import forms
from .models import Minder, User, Booking

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

        Filter user field to only pick pet_owner_user with users role equal to pet minder when creating a Booking on the 
        """
        super().__init__(*args, **kwargs)
        self.fields['pet_owner_user'].queryset = User.objects.filter(role='pet-owner')
