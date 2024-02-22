from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from account.views import TokenObtainPairView

User = get_user_model()


class MyObtainTokenPairViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='test@example.com',
            password='test_password',
            first_name='Test',
            last_name='User'
        )
        self.view = TokenObtainPairView.as_view()
        self.valid_payload = {
            'email': 'test@example.com',
            'password': 'test_password'
        }
        self.invalid_payload = {
            'email': 'test@example.com',
            'password': 'wrong_password'
        }

    def test_obtain_token_pair_view_with_valid_credentials(self):
        response = self.client.post('/account/login/', self.valid_payload, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('refresh', response.data)
        self.assertIn('access', response.data)
        self.assertIn('email', response.data)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertIn('id', response.data)
        self.assertEqual(response.data['id'], self.user.id)
        self.assertIn('first_name', response.data)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertIn('last_name', response.data)
        self.assertEqual(response.data['last_name'], self.user.last_name)

    def test_obtain_token_pair_view_with_invalid_credentials(self):
        response = self.client.post('/account/login/', self.invalid_payload, format='json')
        self.assertEqual(response.status_code, 401)
