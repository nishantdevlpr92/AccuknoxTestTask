from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from account.views import SignUpView

class SignUpAPITestCase(APITestCase):
    def test_signup_success(self):
        url = reverse('sign_up')
        data = {
            "email": "test@example.com",
            "password": "testpassword",
            "first_name": "John",
            "last_name": "Doe"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_signup_existing_email(self):
        # Create a user with a known email
        existing_user = {
            "email": "existing@example.com",
            "password": "testpassword",
            "first_name": "Jane",
            "last_name": "Doe"
        }
        SignUpView().serializer_class().create(existing_user)

        # Attempt to sign up with the same email
        url = reverse('sign_up')
        data = {
            "email": "existing@example.com",
            "password": "newpassword",
            "first_name": "Another",
            "last_name": "User"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0].code, "unique")
    
    def test_signup_with_insensitive_email(self):
        # Create a user with a known email
        existing_user = {
            "email": "existing@example.com",
            "password": "testpassword",
            "first_name": "Jane",
            "last_name": "Doe"
        }
        SignUpView().serializer_class().create(existing_user)

        # Attempt to sign up with the insensitive email
        url = reverse('sign_up')
        data = {
            "email": "EXISTING@EXAMPLE.COM",
            "password": "newpassword",
            "first_name": "Another",
            "last_name": "User"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0].code, "invalid")
