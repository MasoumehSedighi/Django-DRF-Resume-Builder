from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse


class RegisterUserAPITest(TestCase):
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
