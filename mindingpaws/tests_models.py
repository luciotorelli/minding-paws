from django.test import TestCase
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.utils import timezone
from .models import User, Minder, Booking
from datetime import datetime, timedelta


class TestUserModel(TestCase):
    """Test cases for the User model."""

    def test_invalid_role(self):
        """Test creating a User with an invalid role."""
        with self.assertRaises(ValidationError) as context:
            user = User(
                username='testuser',
                email='test@example.com',
                password='testpassword',
                role='invalid-role',
                name='Test User')
            user.full_clean()
        self.assertIn('role', context.exception.message_dict)

    def test_pet_name_max_length(self):
        """Test pet_name exceeding maximum length."""
        long_pet_name = 'A' * 51
        with self.assertRaises(ValidationError) as context:
            user = User(
                username='testuser',
                email='test@example.com',
                password='testpassword',
                role='pet-owner',
                name='Test User',
                pet_name=long_pet_name)
            user.full_clean()
        self.assertIn('pet_name', context.exception.message_dict)

    def test_pet_species_max_length(self):
        """Test pet_species exceeding maximum length."""
        long_pet_species = 'B' * 51
        with self.assertRaises(ValidationError) as context:
            user = User(
                username='testuser',
                email='test@example.com',
                password='testpassword',
                role='pet-owner',
                name='Test User',
                pet_species=long_pet_species)
            user.full_clean()
        self.assertIn('pet_species', context.exception.message_dict)


class TestMinderModel(TestCase):
    """Test cases for the Minder model."""

    def test_minder_valid_data(self):
        """Test creating a valid Minder instance."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            role='minder',
            name='Test User')
        minder = Minder.objects.create(
            user=user,
            bio='Test Bio',
            usual_availability='Test Availability')
        self.assertEqual(str(minder), user.username)

    def test_usual_availability_max_length(self):
        """Test usual_availability exceeding maximum length."""
        long_usual_availability = 'D' * 51
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            role='minder',
            name='Test User')
        with self.assertRaises(ValidationError) as context:
            minder = Minder.objects.create(
                user=user,
                bio='Test Bio',
                usual_availability=long_usual_availability)
            minder.full_clean()
        self.assertIn('usual_availability', context.exception.message_dict)

    def test_minder_deletion(self):
        """Test if Minder instance is deleted
           when associated User is deleted."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            role='minder',
            name='Test User')
        minder = Minder.objects.create(
            user=user,
            bio='Test Bio',
            usual_availability='Test Availability')

        user.delete()

        with self.assertRaises(ObjectDoesNotExist):
            Minder.objects.get(user=minder.user)


class TestBookingModel(TestCase):
    """Test cases for the Booking model."""

    def setUp(self):
        self.pet_owner = User.objects.create_user(
            username='petowner',
            email='petowner@example.com',
            password='testpassword',
            role="pet-owner")
        self.minder_user = User.objects.create_user(
            username='minderuser',
            email='minder@example.com',
            password='testpassword',
            role="minder")
        self.minder = Minder.objects.create(
            user=self.minder_user,
            bio='Test Bio',
            usual_availability='Test Availability')

    def test_minder_name_prepopulated(self):
        """Test if minder_name is prepopulated
           on save based on the minder selected."""
        booking = Booking.objects.create(
            minder=self.minder,
            pet_owner=self.pet_owner,
            start_date=timezone.now(),
            end_date=timezone.now() +
            timedelta(
                hours=2),
            status='pending',
            service_description='Test Service Description',
            pet_name='Test Pet Name',
            pet_species='Test Pet Species')
        self.assertEqual(booking.minder_name, self.minder.user.name)

    def test_pet_owner_name_prepopulated(self):
        """Test if pet_owner_name is prepopulated
           on save based on the pet owner selected."""
        booking = Booking.objects.create(
            minder=self.minder,
            pet_owner=self.pet_owner,
            start_date=timezone.now(),
            end_date=timezone.now() +
            timedelta(
                hours=2),
            status='pending',
            service_description='Test Service Description',
            pet_name='Test Pet Name',
            pet_species='Test Pet Species')
        self.assertEqual(booking.pet_owner_name, self.pet_owner.name)
