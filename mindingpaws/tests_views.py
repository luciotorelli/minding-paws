from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.template.response import TemplateResponse
from .forms import PetOwnerCreationForm, MinderCreationForm


class WelcomeViewTest(TestCase):
    def test_welcome_view_template(self):
        """
        Test that the welcome view uses the correct template.
        """
        response = self.client.get(reverse('welcome'))
        self.assertTemplateUsed(response, 'index.html')


class HomeRedirectViewTest(TestCase):
    def test_authenticated_user_redirect(self):
        """
        Test that an authenticated user is redirected to the 'bookings' page.
        """
        User = get_user_model()  # Get the custom user model
        user = User.objects.create_user(
            username='testuser', password='testpassword')

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('bookings'))

    def test_unauthenticated_user_redirect(self):
        """
        Test that an unauthenticated user is redirected to the 'welcome' page.
        """
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('welcome'))


class AboutUsViewTest(TestCase):
    def test_about_us_view_template(self):
        """
        Test that the AboutUsView uses the correct template.
        """
        response = self.client.get(reverse('about-us'))
        self.assertIsInstance(response, TemplateResponse)
        self.assertTemplateUsed(response, 'about_us.html')

    def test_about_us_view_context(self):
        """
        Test the context data passed to the AboutUsView.
        """
        response = self.client.get(reverse('about-us'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['view'].template_name,
            'about_us.html')


class PetOwnerSignUpViewTest(TestCase):
    def test_pet_owner_sign_up_view_template(self):
        """
        Test that the PetOwnerSignUp view uses the correct template.
        """
        response = self.client.get(reverse('pet-owner-signup'))
        self.assertIsInstance(response, TemplateResponse)
        self.assertTemplateUsed(response, 'account/signup_pet_owner.html')

    def test_pet_owner_sign_up_view_form_class(self):
        """
        Test that the PetOwnerSignUp view uses the correct form class.
        """
        response = self.client.get(reverse('pet-owner-signup'))
        self.assertIsInstance(
            response.context['view'].form_class(),
            PetOwnerCreationForm)


class MinderSignUpViewTest(TestCase):
    def test_minder_sign_up_view_template(self):
        """
        Test that the MinderSignUp view uses the correct template.
        """
        response = self.client.get(reverse('minder-signup'))
        self.assertIsInstance(response, TemplateResponse)
        self.assertTemplateUsed(response, 'account/signup_minder.html')

    def test_minder_sign_up_view_context(self):
        """
        Test the context data passed to the MinderSignUp view.
        """
        response = self.client.get(reverse('minder-signup'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['view'].template_name,
            'account/signup_minder.html')
        self.assertIsInstance(
            response.context['view'].form_class(),
            MinderCreationForm)
