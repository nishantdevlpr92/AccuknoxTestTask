from django.urls import path

from user_hub.views import GetUserList
urlpatterns = [
    path("user-list/", GetUserList.as_view(), name ="user_list"),
   ]