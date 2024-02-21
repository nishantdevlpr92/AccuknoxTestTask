from django_filters import rest_framework as filters

from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from account.models import User
from user_hub.serilizers import SearchUserSerializer
from user_hub.filters import SearchUserFilterSet

class GetUserList(generics.ListAPIView):
    """
        This API returns all user list with pagination.
        Also it is capable to search user bassed on email and name.

        HTTP Methods:
        - GET: Returns all user except requested user.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    serializer_class = SearchUserSerializer
    filter_backends = (filters.DjangoFilterBackend,)

    def list(self, request, *args, **kwargs):
        user_qs = SearchUserFilterSet(
            request.GET,
            queryset=User.objects.exclude(
                id=request.user.id).order_by("-id"),
        )
        page = self.paginate_queryset(user_qs.qs)
        if page is not None:
            serializer = self.serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.serializer_class(user_qs.qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
