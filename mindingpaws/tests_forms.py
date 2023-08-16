from django.test import TestCase
from django.contrib.auth import get_user_model
from .forms import *
from mindingpaws.models import Minder, Booking
from datetime import datetime, timedelta

User = get_user_model()


class TestPetOwnerCreationForm(TestCase):
    """
    Test suite for the PetOwnerCreationForm.
    """

    def test_form_valid_data(self):
        """
        Test form validation with valid data.
        """
        form = PetOwnerCreationForm({
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'name': 'Test User',
            'role': 'pet-owner',
            'pet_name': 'Fluffy',
            'pet_species': 'Dog',
        })
        self.assertTrue(form.is_valid())

    def test_username_already_exists(self):
        """
        Test username already exists validation.
        """
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='existingpassword')
        form = PetOwnerCreationForm({
            'username': 'existinguser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'name': 'Test User',
            'role': 'pet-owner',
            'pet_name': 'Fluffy',
            'pet_species': 'Dog',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors.keys())
        self.assertEqual(
            form.errors['username'][0],
            'A user with that username already exists.')

    def test_max_length_name(self):
        """
        Test max length of name validation.
        """
        form_data = {
            'username': 'testuser',
            'name': 'A' * 100,  # Create a name with 100 characters
            'role': 'pet-owner',
            'pet_name': 'Test Pet',
            'pet_species': 'Dog',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        form = PetOwnerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestMinderCreationForm(TestCase):
    """
    Test suite for the MinderCreationForm.
    """

    def test_form_valid_data(self):
        """
        Test form validation with valid data.
        """
        form = MinderCreationForm({
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'name': 'Test User',
            'bio': 'Test Bio',
            'usual_availability': 'Test Availability',
        })
        self.assertTrue(form.is_valid())

    def test_username_already_exists(self):
        """
        Test username already exists validation.
        """
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='existingpassword')
        form = MinderCreationForm({
            'username': 'existinguser',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
            'name': 'Test User',
            'bio': 'Test Bio',
            'usual_availability': 'Test Availability',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors.keys())
        self.assertEqual(
            form.errors['username'][0],
            'A user with that username already exists.')

    def test_max_length_name(self):
        """
        Test max length of name validation.
        """
        form_data = {
            'username': 'testuser',
            'name': 'A' * 100,  # Create a name with 100 characters
            'bio': 'Test Bio',
            'usual_availability': 'Test Availability',
            'email': 'test@example.com',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        form = MinderCreationForm(data=form_data)
        self.assertTrue(form.is_valid())


class TestBookingCreationForm(TestCase):
    """
    Test suite for the BookingCreationForm.
    """

    def test_form_valid_data(self):
        """
        Test form validation with valid data.
        """
        # Create users for pet owner and minder
        pet_owner = User.objects.create_user(
            username='petowner',
            email='petowner@example.com',
            password='testpassword',
            role="pet-owner")
        minder_user = User.objects.create_user(
            username='minderuser',
            email='minder@example.com',
            password='testpassword',
            role="minder")
        minder = Minder.objects.create(
            user=minder_user,
            bio='Test Bio',
            usual_availability='Test Availability')

        form_data = {
            'minder': minder,
            'pet_owner': pet_owner,
            'start_date': datetime.now() + timedelta(days=1),
            'end_date': datetime.now() + timedelta(days=2),
            'status': 'pending',
            'service_description': 'Test Service Description',
            'pet_name': 'Test Pet Name',
            'pet_species': 'Test Pet Species',
        }

        form = BookingCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_pet_owner_minder_not_empty(self):
        """
        Test that pet owner and minder fields cannot be empty.
        """
        form_data = {
            'start_date': datetime.now() + timedelta(days=1),
            'end_date': datetime.now() + timedelta(days=2),
            'status': 'pending',
            'service_description': 'Test Service Description',
            'pet_name': 'Test Pet Name',
            'pet_species': 'Test Pet Species',
        }

        form = BookingCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('pet_owner', form.errors)
        self.assertIn('minder', form.errors)
