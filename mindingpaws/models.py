from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.TextField(max_length=100)
    ROLE_CHOICES = [
        ('pet-owner', 'Pet Owner'),
        ('minder', 'Minder'),
        ('admin', 'Admin'),
    ]
    role = models.TextField(max_length=9, choices=ROLE_CHOICES)
    pet_name = models.TextField(max_length=50, blank=True, null=True)
    pet_species = models.TextField(max_length=50, blank=True, null=True)

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
        """__str__ This method returns the `username` field from the `User` model.

        Returns:
            str: The username field from the User model
        """
        return self.user.username


class Minder(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500)
    usual_availability = models.TextField(max_length=50)
    photo = CloudinaryField('image', default='placeholder')


class Booking(models.Model):
    minder = models.ForeignKey(Minder, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.TextField(max_length=20)
    service_description = models.TextField(max_length=400)
    pet_name = models.TextField(max_length=50)
    pet_species = models.TextField(max_length=50)
