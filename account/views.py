from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny

from account.serializers import UserSerializer, MyTokenObtainPairSerializer


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    """
    A view class for handling user sign-up requests.

    This class handles POST requests for user sign-up. Upon receiving a POST request,
    it validates the incoming data using the UserSerializer class. If the data is valid,
    a new user is created and saved to the database. Returns a response with the user data
    and a status code of 201 (Created) if the sign-up is successful. If the incoming data
    is invalid, returns a response with the serializer errors and a status code of 400
    (Bad Request).

    Methods:
    ----------
    post(request):
        Handles POST requests for user sign-up.
        Parameters:
            request (Request): The incoming HTTP request.
        Returns:
            Response: The HTTP response containing user data or errors.
    """

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyObtainTokenPairView(TokenObtainPairView):
    """
    Custom view for obtaining a token pair (access token and refresh token).

    This view extends Django Rest Framework's TokenObtainPairView to provide custom
    behavior for token generation. It allows any user (authenticated or unauthenticated)
    to obtain a token pair.
    """

    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer
