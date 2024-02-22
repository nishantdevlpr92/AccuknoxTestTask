from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from django.contrib.auth import get_user_model

from user_hub.models import Friends

User = get_user_model()


class SendFriendRequestAPIViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("send_friend_request")
        self.user1 = User.objects.create_user(
            email='test@example.com',
            password='test_password',
            first_name='Test',
            last_name='User'
        )
        self.user2 =  User.objects.create_user(
            email='test2@example.com',
            password='test_password2',
            first_name='Test 2',
            last_name='User 2'
        )
    def test_send_friend_request(self):
        self.client.force_authenticate(user=self.user1)
        data = {"receiver": self.user2.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Friends.objects.filter(sender=self.user1, receiver=self.user2).exists())

    def test_cannot_send_request_to_self(self):
        self.client.force_authenticate(user=self.user1)
        data = {"receiver": self.user1.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_existing_friend_request(self):
        Friends.objects.create(sender=self.user1, receiver=self.user2)
        self.client.force_authenticate(user=self.user1)
        data = {"receiver": self.user2.id}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
