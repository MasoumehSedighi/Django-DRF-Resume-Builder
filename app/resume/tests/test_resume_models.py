
"""
Tests for resume models
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from resume import models
from django.core.exceptions import ValidationError


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

    def test_create_education(self):
        education = models.Education.objects.create(
            user=self.user,
            institution='Uni',
            degree='Associate',
            start_date='2022-04-12',
            end_date='2024-05-06'
        )
        self.assertEqual(str(education),
                         f'{education.degree} - {education.institution}')

    def test_education_clean_method_invalid(self):
        education = models.Education.objects.create(
            user=self.user,
            institution='Uni',
            degree='Associate',
            start_date='2024-04-12',
            end_date='2022-05-06'
        )
        with self.assertRaises(ValidationError):
            education.clean()

    def test_create_certificate(self):
        certificate = models.Certificate.objects.create(
            user=self.user,
            title='Python Developer',
            issuing_organization='Google',
            issue_date='2024-04-12'
        )
        self.assertEqual(str(certificate),
                         f'{certificate.user} - {certificate.title}')
