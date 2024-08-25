"""
Test for education APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.exceptions import ValidationError
from resume.api import serializers
from resume.models import Education


def detail_url(education_id):
    """Create and return an education detail url."""
    return reverse('resume:education-detail', args=[education_id])


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(email, password)


class EducationAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('resume:education-list')
        self.user = create_user()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(self.url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_education_api(self):
        payload = {
            'user': self.user,
            'institution': 'Test University',
            'degree': 'Bachelor',
            'start_date': '2020-01-01',
            'end_date': '2022-01-01'
        }

        self.client.force_authenticate(user=self.user)

        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['institution'], payload['institution'])
        self.assertEqual(res.data['degree'], payload['degree'])
        self.assertEqual(res.data['start_date'], payload['start_date'])
        self.assertEqual(res.data['end_date'], payload['end_date'])

    def test_education_serializer_validate_end_date(self):
        """
        Test that the validate method raises a ValidationError
          when the start date is after the end date.
        """
        payload = {
            'user': self.user,
            'institution': 'Test University',
            'degree': 'Bachelor',
            'start_date': '2024-01-01',
            'end_date': '2022-01-01'
        }

        with self.assertRaises(ValidationError):
            serializer = serializers.EducationSerializer(data=payload)
            serializer.is_valid(raise_exception=True)

    def test_retrieve_education(self):
        """Test retrieving a list of educations"""
        self.client.force_authenticate(user=self.user)
        Education.objects.create(
            user=self.user,
            institution='Test University',
            degree='Bachelor',
            start_date='2020-02-01',
            end_date='2023-03-01'
        )
        Education.objects.create(
            user=self.user,
            institution='Test College',
            degree='Associate',
            start_date='2022-02-01',
            end_date='2024-03-01'
        )
        self.client.force_authenticate(user=self.user)

        res = self.client.get(self.url)

        educations = Education.objects.all()
        serializer = serializers.EducationSerializer(educations, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_education_list_limited_to_user(self):
        """Test list of educations is limited to authenticated user."""
        other_user = create_user(email="other@example.com")
        Education.objects.create(
            user=other_user,
            institution='Test University',
            degree='Bachelor',
            start_date='2020-02-01',
            end_date='2023-03-01'
        )
        education = Education.objects.create(
            user=self.user,
            institution='Test College',
            degree='Associate',
            start_date='2022-02-01',
            end_date='2024-03-01'
        )

        self.client.force_authenticate(user=self.user)
        res = self.client.get(self.url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['institution'], education.institution)
        self.assertEqual(res.data[0]['degree'], education.degree)
        self.assertEqual(res.data[0]['start_date'], education.start_date)
        self.assertEqual(res.data[0]['end_date'], education.end_date)
        self.assertEqual(res.data[0]['id'], education.id)

    def test_update_education(self):
        """Test updating an education"""
        education = Education.objects.create(
            user=self.user,
            institution='Test College',
            degree='Associate',
            start_date='2022-02-01',
            end_date='2024-03-01'
        )

        payload = {
            'institution': 'Test University',
            'degree': 'Bachelor',
        }
        url = detail_url(education.id)
        self.client.force_authenticate(user=self.user)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        education.refresh_from_db()
        self.assertEqual(education.institution, payload['institution'])
        self.assertEqual(education.degree, payload['degree'])

    def test_delete_education(self):
        """Test deleting an education """
        education = Education.objects.create(
            user=self.user,
            institution='Test College',
            degree='Associate',
            start_date='2022-02-01',
            end_date='2024-03-01'
        )
        self.client.force_authenticate(user=self.user)
        url = detail_url(education.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        education_exists = Education.objects.filter(user=self.user).exists()
        self.assertFalse(education_exists)
