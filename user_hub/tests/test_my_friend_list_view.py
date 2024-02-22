from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate
from user_hub.views import MyFriendListView
from django.contrib.auth import get_user_model

from user_hub.models import Friends

User = get_user_model()

class MyFriendListViewTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            email='test@example.com',
            password='test_password',
            first_name='Test',
            last_name='User'
        )
        # Initialize RequestFactory
        self.factory = RequestFactory()

    def test_get_friend_list(self):
        # Create some friends for the user
        friend1 = User.objects.create_user(
            email='test1@example.com',
            password='test_password1',
            first_name='John',
            last_name='User 1'
        )
        friend2 = User.objects.create_user(
            email='test2@example.com',
            password='test_password2',
            first_name='Test 2',
            last_name='User 2'
        )
        # Assuming friend1 and friend2 are accepted friends of the user
        # You may need to adjust this according to your model logic
        # Here, we're not going through the friend request process
        
        # Create friends instances (assuming your Friends model exists)
        Friends.objects.create(sender=self.user, receiver=friend1, status='accepted')
        Friends.objects.create(sender=self.user, receiver=friend2, status='accepted')
        
        # Create a GET request to the API endpoint
        request = self.factory.get('my-friend-list/')
        
        # Force authenticate the request with the user
        force_authenticate(request, user=self.user)
        
        # Initialize the API view with the request
        view = MyFriendListView.as_view()
        response = view(request)
        
        # Check if the response is successful (status code 200)
        self.assertEqual(response.status_code, 200)
        
        # Check if the response data contains the correct number of friends
        self.assertEqual(len(response.data['results']), 2)
