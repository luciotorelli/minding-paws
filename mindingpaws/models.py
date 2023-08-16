from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from cloudinary.models import CloudinaryField
from django.utils import timezone


class User(AbstractUser):
    """
    Custom user model with extended fields
    """
    name = models.CharField(max_length=40, blank=False, null=False)
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
        """
        Validate the user's fields based on their role.

        Raises:
            ValidationError: If pet_name or pet_species
                is empty for pet owners.
        """
        if self.role == 'pet-owner' and not self.pet_name:
            raise ValidationError("Pet name is required for Pet Owners.")
        if self.role == 'pet-owner' and not self.pet_species:
            raise ValidationError("Pet species is required for Pet Owners.")

    def __str__(self):
        """
        Get a human-readable representation of the user.

        Returns:
            str: The username of the user.
        """
        return self.username


class Minder(models.Model):
    """
    Model to represent a pet minder with their details.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=False, null=False)
    usual_availability = models.CharField(
        max_length=50,
        help_text="Example: Monday to Friday, 10am to 6pm.",
        blank=False,
        null=False)
    photo = CloudinaryField(
        'image',
        default='https://res.cloudinary.com/dls3mbdix/image/upload/ \
                 v1690889814/static/img/profile-placeholder_hgqisr.webp',
        null=True,
        blank=True)

    def __str__(self):
        """
        Get a human-readable representation of the minder.

        Returns:
            str: The username of the associated user.
        """
        return self.user.username


class Booking(models.Model):
    """
    Model to represent a booking for pet care services.
    """
    minder = models.ForeignKey(Minder, on_delete=models.SET_NULL, null=True)
    pet_owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    minder_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="This field will be prepopulated \
                   on save based on the minder selected")
    pet_owner_name = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="This field will be prepopulated \
                   on save based on the pet owner selected")
    start_date = models.DateTimeField(blank=False, null=False)
    end_date = models.DateTimeField(blank=False, null=False)
    STATUS_CHOICES = [
        ('accepted', 'Accepted'),
        ('pending', 'Pending'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed')
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        blank=False,
        null=False)
    service_description = models.TextField(
        max_length=400, blank=False, null=False)
    pet_name = models.CharField(max_length=50, blank=False, null=False)
    pet_species = models.CharField(max_length=50, blank=False, null=False)

    def save(self, *args, **kwargs):
        """
        Save method to prepopulate pet owner name and minder name.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        if self.pet_owner:
            self.pet_owner_name = self.pet_owner.name
        if self.minder and self.minder.user:
            self.minder_name = self.minder.user.name

        super(Booking, self).save(*args, **kwargs)

    def clean(self):
        """
        Validate booking fields.

        Raises:
            ValidationError: If any validation fails.
        """
        self.clean_pet_owner_and_minder()
        self.clean_start_date()
        self.clean_end_date()

    def clean_pet_owner_and_minder(self):
        """
        Verify that the pet owner and minder are not the same user.

        Raises:
            ValidationError: If pet owner is the same as the minder.
        """
        if self.minder and self.pet_owner == self.minder.user:
            raise ValidationError(
                "The pet owner cannot be the same as the minder.")

    def clean_start_date(self):
        """
        Verify that the start date is not in the past.

        Raises:
            ValidationError: If start date is in the past.
        """
        if self.start_date and self.start_date < timezone.now():
            raise ValidationError("Start date cannot be in the past.")

    def clean_end_date(self):
        """
        Verify that the end date is not prior to the start date.

        Raises:
            ValidationError: If end date is prior to start date.
        """
        if self.start_date and self.end_date < self.start_date:
            raise ValidationError(
                "Select an end date later than the start date.")

    def __str__(self):
        """
        Get a human-readable representation of the booking.

        Returns:
            str: The username of the associated pet owner.
        """
        return self.pet_owner.username
