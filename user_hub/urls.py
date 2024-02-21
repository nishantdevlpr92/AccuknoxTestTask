from django.urls import path

from user_hub.views import GetUserList, MyFriendListView

urlpatterns = [
    path("user-list/", GetUserList.as_view(), name="user_list"),
    path("my-friend-list/", MyFriendListView.as_view(), name="my-friend-list"),
]