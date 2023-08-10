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

class PetOwnerProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'pet_name', 'pet_species']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'pet_name': forms.TextInput(attrs={'class': 'form-control'}),
            'pet_species': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Username',
            'email': 'Email Address',
            'name': 'Owner Name',
            'pet_name': 'Pet Name',
            'pet_species': 'Pet Species',
        }

class MinderProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Username')
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Email Address', max_length=100)
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Minder Name', max_length=100)
    bio = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), label='Bio', max_length=500)
    usual_availability = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), label='Usual Availability', max_length=50)
    photo = CloudinaryFileField(
        options={
            'folder': 'static/img/minders',
            'resource_type': 'image'
        },
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        label='Profile Photo'
    )

    class Meta:
        model = Minder
        fields = ['bio', 'usual_availability', 'photo']

    def __init__(self, *args, user_instance=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_instance = user_instance
        self.fields['email'].initial = user_instance.email
        self.fields['name'].initial = user_instance.name
        try:
            minder_instance = Minder.objects.get(user=user_instance)
            self.fields['bio'].initial = minder_instance.bio
            self.fields['usual_availability'].initial = minder_instance.usual_availability
            self.fields['photo'].initial = minder_instance.photo
        except Minder.DoesNotExist:
            pass

    def save(self, commit=True):
        instance = super().save(commit=False)
        self.user_instance.email = self.cleaned_data['email']
        self.user_instance.name = self.cleaned_data['name']
        self.user_instance.save()
        if commit:
            instance.save()
        return instance

    def clean(self):
        cleaned_data = super().clean()
        bio = cleaned_data.get('bio')
        usual_availability = cleaned_data.get('usual_availability')
        
        if not bio:
            self.add_error('bio', 'Bio is required.')
        if not usual_availability:
            self.add_error('usual_availability', 'Usual Availability is required.')