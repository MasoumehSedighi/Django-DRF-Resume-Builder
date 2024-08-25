"""
Test for Resume API.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from accounts.models import Profile
from resume.models import (
    Skill,
    Education,
    Certificate,
    Experience,
)


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(email, password)


class ResumeAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('resume:resume-detail', args=[1])
        self.user = create_user()
        self.profile = Profile.objects.get(user=self.user)
        self.skill = Skill.objects.create(user=self.user, title='Python')
        self.education = Education.objects.create(
            user=self.user,
            institution='Tech Uni',
            degree='Bachelor',
            start_date='2020-01-01',
            end_date='2023-01-01'
        )
        self.certificate = Certificate.objects.create(
            user=self.user,
            title='Django Developer',
            issuing_organization='Django Institute',
            issue_date='2023-06-01'
        )
        self.experience = Experience.objects.create(
            user=self.user,
            company='Tech Group',
            position='Software Engineer',
            description='Worked on developing applications.',
            start_date='2022-04-12',
            end_date='2023-05-06'
        )

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(self.url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_resume(self):
        """Test retrieving all resume-related data
           for the authenticated user.
        """

        self.client.force_authenticate(user=self.user)
        res = self.client.get(self.url)

        self.assertEqual(res.data['email'], self.user.email)
        self.assertEqual(len(res.data['skills']), 1)
        self.assertEqual(len(res.data['educations']), 1)
        self.assertEqual(len(res.data['certificates']), 1)
        self.assertEqual(len(res.data['experiences']), 1)
        self.assertEqual(
            res.data['profile']['first_name'],
            self.profile.first_name
        )
        self.assertEqual(
            res.data['profile']['last_name'],
            self.profile.last_name
        )
        self.assertEqual(
            res.data['profile']['about_me'],
            self.profile.about_me
        )
