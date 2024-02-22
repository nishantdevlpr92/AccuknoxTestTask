from rest_framework.test import APIClient, APIRequestFactory, force_authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model

from user_hub.views import AcceptRejectRequestAPIView
from user_hub.models import Friends

User = get_user_model()


class AcceptRejectRequestAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.factory = APIRequestFactory()

        self.user = User.objects.create_user(
            email='test@example.com',
            password='test_password',
            first_name='Test',
            last_name='User'
        )
        self.friend = User.objects.create_user(
            email='test2@example.com',
            password='test_password2',
            first_name='Test 2',
            last_name='User 2'
        )
        self.friend_id = Friends.objects.create(sender=self.friend, receiver=self.user, status='pending')

    def test_accept_request(self):
        url = reverse('accept_reject_request', kwargs={'friend_id': self.friend_id.id})
        data = {'status': 'accepted'}
        request = self.factory.patch(url, data=data)
        force_authenticate(request, user=self.user)
        response = AcceptRejectRequestAPIView.as_view()(request, friend_id=self.friend_id.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'accepted')

    def test_reject_request(self):
        url = reverse('accept_reject_request', kwargs={'friend_id': self.friend_id.id})
        data = {'status': 'rejected'}
        request = self.factory.patch(url, data=data)
        force_authenticate(request, user=self.user)
        response = AcceptRejectRequestAPIView.as_view()(request, friend_id=self.friend_id.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['status'], 'rejected')

    def test_unauthorized_request(self):
        # Testing unauthorized request
        url = reverse('accept_reject_request', kwargs={'friend_id': self.friend_id.id})
        data = {'status': 'accepted'}
        request = self.factory.patch(url, data=data)
        response = AcceptRejectRequestAPIView.as_view()(request, friend_id=self.friend_id.pk)
        self.assertEqual(response.status_code, 401)

    def test_invalid_status(self):
        url = reverse('accept_reject_request', kwargs={'friend_id': self.friend_id.id})
        data = {'status': 'invalid_status'}
        request = self.factory.patch(url, data=data)
        force_authenticate(request, user=self.user)
        response = AcceptRejectRequestAPIView.as_view()(request, friend_id=self.friend_id.pk)
        self.assertEqual(response.status_code, 400)

    def test_nonexistent_friend(self):
        # Testing request for nonexistent friend
        url = reverse('accept_reject_request', kwargs={'friend_id': self.friend_id.id + 1})
        data = {'status': 'accepted'}
        request = self.factory.patch(url, data=data)
        force_authenticate(request, user=self.user)
        response = AcceptRejectRequestAPIView.as_view()(request, friend_id=self.friend_id.pk + 1)
        self.assertEqual(response.status_code, 404)
