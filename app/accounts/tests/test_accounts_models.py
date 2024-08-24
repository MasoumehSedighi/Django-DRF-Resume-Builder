"""
Tests for User model
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from accounts.models import Profile


class TestUserModel(TestCase):
    """Test User model"""
    def test_create_user(self):
        """Test Creating a user with email."""
        user = get_user_model().objects.create_user(
            email="test@example.com",
            password="test@123"
        )
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("test@123"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            get_user_model().objects.create_user()
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email="")
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(email="", password="test@123")

    def test_create_superuser(self):
        """Test Creating a superuser with email."""
        admin_user = get_user_model().objects.create_superuser(
            email="admin@example.com",
            password="test@123"
        )
        self.assertEqual(admin_user.email, "admin@example.com")
        self.assertTrue(admin_user.check_password("test@123"))
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            get_user_model().objects.create_superuser(
                email="admin@example.com",
                password="test@123",
                is_superuser=False
            )


class ProfileModelTest(TestCase):
    """
    Test for the Profile model.
    """

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password="passtest123"
        )

    def test_create_profile(self):
        """
        Test that a profile instance is created whenever
        a User instance is created
        """
        profile = Profile.objects.get(user=self.user)
        self.assertIsInstance(profile, Profile)
        self.assertEqual(str(profile), self.user.email)
