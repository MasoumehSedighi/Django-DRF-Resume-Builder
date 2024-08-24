from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from accounts.models import Profile


class RegisterUserAPITests(TestCase):
    """Tests for the RegisterUserView."""

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('accounts:register')

    def test_register_user_success(self):
        """Test registering a user is successful."""

        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'password1': 'testpass123'
        }

        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)
        self.assertNotIn('password1', res.data)

    def test_register_user_passwords_do_not_match(self):
        """Test error is returned if passwords do not match"""

        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'password1': 'wrongpass123'
        }

        res = self.client.post(self.url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 6 chars."""

        payload = {
            'email': 'test@example.com',
            'password': 'test',
            'password1': 'test'
        }
        res = self.client.post(self.url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_user_with_exists_error(self):
        """Test error returned if user with email exists."""

        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'password1': 'testpass123'
        }

        get_user_model().objects.create_user(
            email=payload['email'], password=payload["password"])
        res = self.client.post(self.url, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_regster_user_missing_field(self):
        """
        Test registration fails when a required field is missing.
        """

        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
        }

        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password1', res.data)


class TokenAPITests(TestCase):
    """
    Test for a new authentication token for a user.
    """

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123',
        )
        self.url = reverse('accounts:token')

    def test_create_token_for_user(self):
        """Test generates token for valid credentials."""

        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
        }
        res = self.client.post(self.url, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credential(self):
        """Test returns error if credentials invalid."""

        payload = {
            'email': 'test@example.com',
            'password': 'badpass123'
        }

        res = self.client.post(self.url, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class ProfileAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123',
        )
        self.url = reverse('accounts:profile')

    def test_retrive_profile_unauthorize(self):
        """Test authentication is required for user's profile."""

        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrive_profile_success(self):
        """Test retriving profile for logged in user."""
        self.client.force_authenticate(user=self.user)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'email': self.user.email,
            'first_name': None,
            'last_name': None,
            'about_me': None
        })

    def test_update_profile(self):
        """Test updating the user profile for the authenticated user."""

        self.client.force_authenticate(user=self.user)
        payload = {
            'first_name': 'test',
            'last_name': 'last_test',
            'about_me': 'This is my profile'
        }
        profile = Profile.objects.get(user=self.user)
        res = self.client.patch(self.url, payload)
        profile.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(profile.first_name, payload['first_name'])
        self.assertEqual(profile.last_name, payload['last_name'])
        self.assertEqual(profile.about_me, payload['about_me'])
