"""
Test for skill APIs.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from resume.api import serializers
from resume.models import (
    Skill,
)


def detail_url(skill_id):
    """Create and return a skill detail url."""
    return reverse('resume:skill-detail', args=[skill_id])


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(email, password)


class SkillAPITests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('resume:skill-list')
        self.user = create_user()

    def test_auth_required(self):
        """Test auth is required to call API."""
        res = self.client.get(self.url)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrive_skill(self):
        """Test retrieving a list of skills"""
        self.client.force_authenticate(user=self.user)
        Skill.objects.create(user=self.user, title='Python')
        Skill.objects.create(user=self.user, title='Django')

        res = self.client.get(self.url)

        skills = Skill.objects.all()
        serializer = serializers.SkillSerializer(skills, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_skill_list_limited_to_user(self):
        """Test list of skills is limited to authenticated user."""
        other_user = create_user(email="other@example.com")
        Skill.objects.create(user=other_user, title='Java')
        skill = Skill.objects.create(user=self.user, title='Django')

        self.client.force_authenticate(user=self.user)
        res = self.client.get(self.url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], skill.title)
        self.assertEqual(res.data[0]['id'], skill.id)

    def test_update_skill(self):
        """Test updating a skill"""
        skill = Skill.objects.create(user=self.user, title='Django')

        payload = {'title': 'Django Rest Framework'}
        url = detail_url(skill.id)
        self.client.force_authenticate(user=self.user)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        skill.refresh_from_db()
        self.assertEqual(skill.title, payload['title'])

    def test_delete_skill(self):
        """Test deleting a skill """
        skill = Skill.objects.create(user=self.user, title='Django')
        self.client.force_authenticate(user=self.user)
        url = detail_url(skill.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        skill_exists = Skill.objects.filter(user=self.user).exists()
        self.assertFalse(skill_exists)
