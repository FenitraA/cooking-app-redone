from datetime import datetime, timezone
from rest_framework_simplejwt.settings import api_settings

from django.conf import settings
from django.contrib.auth import authenticate

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserLoginSerializer
from users.throttles import LoginRateThrottle, RefreshRateThrottle


class LoginView(APIView):
    throttle_classes = [LoginRateThrottle]
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        request=UserLoginSerializer,
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(
            username=username,
            password=password,
        )

        if user is None:
            return Response(
                {"detail": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token

        now = datetime.now(timezone.utc)

        response = Response(
            {
                "detail": "Login successful",
            }
        )

        response.set_cookie(
            key="access_token",
            value=str(access),
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=int(api_settings.ACCESS_TOKEN_LIFETIME.total_seconds()),
        )

        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=int(api_settings.REFRESH_TOKEN_LIFETIME.total_seconds()),
        )

        return response


class RefreshView(APIView):
    throttle_classes = [RefreshRateThrottle]
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response(
                {"detail": "No refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            refresh = RefreshToken(refresh_token)
        except Exception:
            return Response(
                {"detail": "Invalid refresh token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        response = Response(
            {
                "detail": "Token refreshed",
            }
        )

        response.set_cookie(
            key="access_token",
            value=str(refresh.access_token),
            httponly=True,
            secure=False,
            samesite="Lax",
        )

        return response


class LogoutView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        response = Response(
            {
                "detail": "Logout successful",
            }
        )

        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response
