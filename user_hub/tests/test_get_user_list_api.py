from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class GetUserListTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            email='test@example.com',
            password='test_password',
            first_name='Test',
            last_name='User'
        )
        # Create some users for testing
        self.user1 = User.objects.create_user(
            email='test1@example.com',
            password='test_password1',
            first_name='John',
            last_name='User 1'
        )
        self.user2 = User.objects.create_user(
            email='test2@example.com',
            password='test_password2',
            first_name='Test 2',
            last_name='User 2'
        )
        # Authenticate the test user
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_user_list(self):
        response = self.client.get('/api/user-list/')

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the correct number of users are returned
        self.assertEqual(len(response.data['results']), 2)

        # Check that the serializer fields are present
        self.assertIn('email', response.data['results'][0])
        self.assertIn('first_name', response.data['results'][0])
        self.assertIn('last_name', response.data['results'][0])

    def test_pagination(self):
        # Assuming that the number of users exceeds the default pagination limit
        for i in range(10):
            User.objects.create_user(email=f'user{i}@example.com', first_name=f'User{i}', last_name=str(i))

        response = self.client.get('/api/user-list/')

        # Check that pagination is working correctly
        self.assertIn('count', response.data)
        self.assertIn('next', response.data)
        self.assertIn('previous', response.data)
        self.assertIn('results', response.data)

    def test_filtering(self):
        response = self.client.get('/api/user-list/?search=John')

        # Check that filtering is working correctly
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['first_name'], 'John')

    def test_permissions(self):
        # Test when user is not authenticated
        self.client.force_authenticate(user=None)
        response = self.client.get('/api/user-list/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Test when user is authenticated
        self.client.force_authenticate(user=self.user)
        response = self.client.get('/api/user-list/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
