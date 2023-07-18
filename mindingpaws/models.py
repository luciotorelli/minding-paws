from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField
from django.utils import timezone


class User(AbstractUser):
    name = models.CharField(max_length=40)
    ROLE_CHOICES = [
        ('pet-owner', 'Pet Owner'),
        ('minder', 'Minder'),
        ('admin', 'Admin'),
    ]
    role = models.CharField(
        max_length=9, choices=ROLE_CHOICES, blank=False, null=False)
    pet_name = models.CharField(max_length=50, blank=True, null=True)
    pet_species = models.CharField(max_length=50, blank=True, null=True)

    def clean(self):
        """clean If the role field is set to pet-owner, confirm that pet_name
        and pet_species are not empty.

        Raises:
            ValidationError: Raises ValidationError if Pet name is empty and role field is Pet Owner.
            ValidationError: Raises ValidationError if Pet species is empty and role field is Pet Owner.
        """
        if self.role == 'pet-owner' and not self.pet_name:
            raise ValidationError("Pet name is required for Pet Owners.")
        if self.role == 'pet-owner' and not self.pet_species:
            raise ValidationError("Pet species is required for Pet Owners.")

    def __str__(self):
        """__str__ This method returns the `username` field from the `User` model in a readable format.

        Returns:
            str: The username field from the User model
        """
        return self.username

class Minder(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)
    usual_availability = models.CharField(max_length=50, help_text="Example: Monday to Friday, 10am to 6pm.")
    photo = CloudinaryField('image', default='placeholder')

    def __str__(self):
        """__str__ This method returns the `username` field from the `User` model in a readable format.

        Returns:
            str: The username field from the User model
        """
        return self.user.username


class Booking(models.Model):
    minder = models.ForeignKey(Minder, on_delete=models.SET_NULL, null=True)
    pet_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    minder_name = models.CharField(max_length=100, blank=True, null=True, help_text="This field will be prepopulated on save based on the minder selected")
    pet_owner_name = models.CharField(max_length=100, blank=True, null=True, help_text="This field will be prepopulated on save based on the pet owner selected")
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    STATUS_CHOICES = [
        ('accepted', 'Accepted'),
        ('pending', 'Pending'),
        ('declined', 'Declined'),
        ('completed', 'Completed')
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    service_description = models.TextField(max_length=400)
    pet_name = models.CharField(max_length=50)
    pet_species = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        """save redefine save

        prepopulate pet owner name and minder name based on user selected when being saved, 
        this allows for Users to be deleted without affecting the booking database.
        """
        if self.pet_owner:
            self.pet_owner_name = self.pet_owner.name
        if self.minder and self.minder.user:
            self.minder_name = self.minder.user.name

        super(Booking, self).save(*args, **kwargs)

    def clean(self):
        """Validation for booking fields.

        Raises:
            ValidationError: Raises a validation error if any of the validations fails.
        """
        self.clean_pet_owner_and_minder()
        self.clean_start_date()
        self.clean_end_date()

    def clean_pet_owner_and_minder(self):
        """Verify if Pet Owner is not the same user as the minder

        Raises:
            ValidationError: Raises a validation error if the pet owner is the same user as the minder being booked.
        """
        if self.minder and self.pet_owner == self.minder.user:
            raise ValidationError(
                "The pet owner cannot be the same as the minder.")

    def clean_start_date(self):
        """Verify if start date is not in the past

        Raises:
            ValidationError: Raises a validation error if start date is less than the current date
        """
        if self.start_date < timezone.now():
            raise ValidationError("Start date can not be in the past.")

    def clean_end_date(self):
        """Verify if end_date is not set prior to the start_date

        Raises:
            ValidationError: Raises a validation error if end_date is prior to start_date
        """
        if self.end_date < self.start_date:
            raise ValidationError(
                "Select an end date later than the start date.")

    def __str__(self):
        """__str__ This method returns the `username` field from the `User` model in a readable format.

        Returns:
            str: The username field of the pet owner
        """
        return self.pet_owner.username
