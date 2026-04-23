from django.urls import path
from accounts.api.views import RegisterView,LogoutApi
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView

urlpatterns = [
    path("register/",RegisterView.as_view(), name="register"),
    path("login/",TokenObtainPairView.as_view()),
    path("refresh/",TokenRefreshView.as_view()),
    path("logout/", LogoutApi.as_view()),

]