from django.urls import path

from user_hub.views import (
    GetUserList, 
    MyFriendListView, 
    FriendRequestListView,
    SendFriendRequestAPIView,
    AcceptRejectRequestAPIView,
)

urlpatterns = [
    path("user-list/", GetUserList.as_view(), name="user_list"),
    path(
        "my-friend-list/", 
        MyFriendListView.as_view(), 
        name="my_friend_list"
    ),
    path(
        "friend-request-list/", 
        FriendRequestListView.as_view(), 
        name="friend_request_list"
    ),
    path(
        "send-friend-request/",
        SendFriendRequestAPIView.as_view(),
        name="send-friend-request",
    ),
    path(
        "accept-reject-request/<int:friend_id>/",
        AcceptRejectRequestAPIView.as_view(),
        name="accept_reject_request",
    ),

]