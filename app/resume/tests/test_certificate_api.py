"""
Test for certificate APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from resume.api import serializers
from resume.models import Certificate


def detail_url(certificate_id):
    """Create and return a certificate detail url."""
    return reverse('resume:certificate-detail', args=[certificate_id])


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(email, password)


class CertificateAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('resume:certificate-list')
        self.user = create_user()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(self.url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_certificate_api(self):
        """Test creating a certificate"""

        payload = {
            'user': self.user,
            'title': 'Machine Learning Expert',
            'issuing_organization': 'ML Institute',
            'issue_date': '2024-01-12'
        }

        self.client.force_authenticate(user=self.user)

        res = self.client.post(self.url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['title'], payload['title'])
        self.assertEqual(
            res.data['issuing_organization'],
            payload['issuing_organization']
        )
        self.assertEqual(res.data['issue_date'], payload['issue_date'])

    def test_retrive_certificate(self):
        """Test retrieving a list of certificates"""
        self.client.force_authenticate(user=self.user)
        Certificate.objects.create(
            user=self.user,
            title='Machine Learning Expert',
            issuing_organization='ML Institute',
            issue_date='2024-01-12'
        )
        Certificate.objects.create(
            user=self.user,
            title='Python Developer',
            issuing_organization='Google',
            issue_date='2024-04-12'
        )

        res = self.client.get(self.url)

        certificates = Certificate.objects.all()
        serializer = serializers.CertificateSerializer(certificates, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_certificate_list_limited_to_user(self):
        """Test list of certificates is limited to authenticated user."""
        other_user = create_user(email="other@example.com")
        Certificate.objects.create(
            user=other_user,
            title='Python Developer',
            issuing_organization='Google',
            issue_date='2024-04-12'
        )
        certificate = Certificate.objects.create(
            user=self.user,
            title='Machine Learning Expert',
            issuing_organization='ML Institute',
            issue_date='2024-01-12'
        )

        self.client.force_authenticate(user=self.user)
        res = self.client.get(self.url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], certificate.title)
        self.assertEqual(
            res.data[0]['issuing_organization'],
            certificate.issuing_organization
        )
        self.assertEqual(res.data[0]['issue_date'], certificate.issue_date)
        self.assertEqual(res.data[0]['id'], certificate.id)

    def test_update_certificate(self):
        """Test updating a certificate"""
        certificate = Certificate.objects.create(
            user=self.user,
            title='Python Developer',
            issuing_organization='Google',
            issue_date='2024-04-12'
        )

        payload = {
            'title': 'Java Developer',
            'issuing_organization': 'Java Institute',
        }
        url = detail_url(certificate.id)
        self.client.force_authenticate(user=self.user)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        certificate.refresh_from_db()
        self.assertEqual(certificate.title, payload['title'])
        self.assertEqual(
            certificate.issuing_organization,
            payload['issuing_organization']
        )

    def test_delete_certificate(self):
        """Test deleting a certificate """
        certificate = Certificate.objects.create(
            user=self.user,
            title='Python Developer',
            issuing_organization='Google',
            issue_date='2024-04-12'
        )
        self.client.force_authenticate(user=self.user)
        url = detail_url(certificate.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        certificate_exists = Certificate.objects.filter(
            user=self.user
            ).exists()
        self.assertFalse(certificate_exists)
