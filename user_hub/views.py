from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from django.db.models import Case, F, IntegerField, Q, Value, When

from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle

from account.models import User
from user_hub.serilizers import SearchUserSerializer, FriendDataSerializer
from user_hub.filters import SearchUserFilterSet
from user_hub.models import Friends


class GetUserList(generics.ListAPIView):
    """
    This API returns all user list with pagination.
    Also it is capable to search user bassed on email and name.

    query_param:
        search:CharField

    HTTP Methods:
    - GET: Returns all user except requested user.
    """

    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    serializer_class = SearchUserSerializer
    filter_backends = (filters.DjangoFilterBackend,)

    def list(self, request, *args, **kwargs):
        user_qs = SearchUserFilterSet(
            request.GET,
            queryset=User.objects.exclude(id=request.user.id))
        page = self.paginate_queryset(user_qs.qs)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(user_qs.qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyFriendListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SearchUserSerializer
    pagination_class = PageNumberPagination
    """
    This API view is used to get the list of accepted friends for the authenticated user.
    """

    def get(self, request, *args, **kwargs):
        user_qs = User.objects.filter(
            id__in=self.get_friend_list_based_on_given_user(request.user)
        )
        page = self.paginate_queryset(user_qs)
        serializer = (
            self.serializer_class(page, many=True)
            if page
            else self.serializer_class(user_qs, many=True)
        )
        return (
            self.get_paginated_response(serializer.data)
            if page
            else Response(serializer.data, status=status.HTTP_200_OK)
        )

    def get_friend_list_based_on_given_user(self, user):
        """
        get the subquery for accepted friends based on the given user.
        """
        return (
            Friends.objects.filter(Q(sender=user) | Q(receiver=user), status="accepted")
            .annotate(
                accepted_user_ids=Case(
                    When(sender=user, then=F("receiver__id")),
                    When(receiver=user, then=F("sender__id")),
                    default=Value(0),
                    output_field=IntegerField(),
                )
            )
            .values("accepted_user_ids")
        )


class SendFriendRequestAPIView(generics.CreateAPIView):
    serializer_class = FriendDataSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    __doc__ = """
            This API is used to send the friend request to the other user
            param:
                receiver: receiver user id
    """

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        sender = self.request.user
        serializer.validated_data["sender"] = sender
        # Ensure that the receiver exists and is not the sender
        receiver_id = serializer.validated_data["receiver"]
        if receiver_id == sender.id:
            return Response(
                {"detail": "Cannot send friend request to yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Ensure that there is no existing friend request between the sender and receiver
        existing_request = Friends.objects.filter(
            sender=sender, receiver_id=receiver_id
        ).exists()
        if existing_request:
            return Response(
                {"detail": "Friend request already sent."}, status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)