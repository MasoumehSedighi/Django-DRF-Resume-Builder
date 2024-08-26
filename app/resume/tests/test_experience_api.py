"""
Test for experience APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.exceptions import ValidationError
from resume.api import serializers
from resume.models import Experience


def detail_url(experience_id):
    """Create and return an experience detail url."""
    return reverse('resume:experience-detail', args=[experience_id])


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(email, password)


class ExperienceAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('resume:experience-list')
        self.user = create_user()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(self.url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_experience_api(self):
        """Test creating an experience"""

        payload = {
            'company': 'Tech Group',
            'position': 'Software Engineer',
            'description': 'Worked on developing applications.',
            'start_date': '2022-04-12',
            'end_date': '2023-05-06'
        }

        self.client.force_authenticate(user=self.user)

        res = self.client.post(self.url, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['company'], payload['company'])
        self.assertEqual(res.data['position'], payload['position'])
        self.assertEqual(res.data['description'], payload['description'])
        self.assertEqual(res.data['start_date'], payload['start_date'])
        self.assertEqual(res.data['end_date'], payload['end_date'])

    def test_experience_serializer_validate_end_date(self):
        """
        Test that the validate method raises a ValidationError
        when the start date is after the end date.
        """
        payload = {
            'user': self.user,
            'company': 'Tech Group',
            'position': 'Software Engineer',
            'description': 'Worked on developing applications.',
            'start_date': '2023-04-12',
            'end_date': '2022-05-06'
        }

        with self.assertRaises(ValidationError):
            serializer = serializers.ExperienceSerializer(data=payload)
            serializer.is_valid(raise_exception=True)

    def test_retrieve_experience(self):
        """Test retrieving a list of experiences"""

        self.client.force_authenticate(user=self.user)
        Experience.objects.create(
            user=self.user,
            company='Sky Group',
            position='Python Developer',
            description='Worked on Python apps.',
            start_date='2023-02-01',
            end_date='2024-05-06'
        )
        Experience.objects.create(
            user=self.user,
            company='Tech Group',
            position='Software Engineer',
            description='Worked on developing applications.',
            start_date='2023-04-12',
            end_date='2022-05-06'
        )
        self.client.force_authenticate(user=self.user)

        res = self.client.get(self.url)

        experiences = Experience.objects.all()
        serializer = serializers.ExperienceSerializer(experiences, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_experience_list_limited_to_user(self):
        """Test list of experiences is limited to authenticated user."""

        other_user = create_user(email="other@example.com")
        Experience.objects.create(
            user=other_user,
            company='Tech Group',
            position='Software Engineer',
            description='Worked on developing applications.',
            start_date='2022-04-12',
            end_date='2023-05-06'
        )
        experience = Experience.objects.create(
            user=self.user,
            company='Sky Group',
            position='Python Developer',
            description='Worked on Python apps.',
            start_date='2023-02-01',
            end_date='2024-05-06'
        )

        self.client.force_authenticate(user=self.user)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['company'], experience.company)
        self.assertEqual(res.data[0]['position'], experience.position)
        self.assertEqual(res.data[0]['description'], experience.description)
        self.assertEqual(res.data[0]['start_date'], experience.start_date)
        self.assertEqual(res.data[0]['end_date'], experience.end_date)
        self.assertEqual(res.data[0]['id'], experience.id)

    def test_update_experience(self):
        """Test updating an experience"""

        experience = Experience.objects.create(
            user=self.user,
            company='Sky Group',
            position='Python Developer',
            description='Worked on Python apps.',
            start_date='2023-02-01',
            end_date='2024-05-06'
        )

        payload = {
            'company': 'Tech Group',
            'position': 'Software Engineer',
        }
        url = detail_url(experience.id)
        self.client.force_authenticate(user=self.user)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        experience.refresh_from_db()
        self.assertEqual(experience.company, payload['company'])
        self.assertEqual(experience.position, payload['position'])

    def test_delete_experience(self):
        """Test deleting an experience """
        experience = Experience.objects.create(
            user=self.user,
            company='Sky Group',
            position='Python Developer',
            description='Worked on Python apps.',
            start_date='2023-02-01',
            end_date='2024-05-06'
        )
        self.client.force_authenticate(user=self.user)
        url = detail_url(experience.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        experience_exists = Experience.objects.filter(user=self.user).exists()
        self.assertFalse(experience_exists)
