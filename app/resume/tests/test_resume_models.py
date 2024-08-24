
"""
Tests for resume models
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from resume import models


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


class ResumeModelsTests(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='testpass123'
        )

    def test_create_skill(self):
        skill = models.Skill.objects.create(
            user=self.user,
            title='Python'
        )
        self.assertEqual(str(skill), f'{skill.user} - {skill.title}')
