from django.urls import path
from rest_framework_simplejwt.views import  TokenRefreshView

from account.views import SignUpView, MyObtainTokenPairView

urlpatterns = [
    path("sign-up/", SignUpView.as_view(), name ="sign_up"),
    path("login/", MyObtainTokenPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]