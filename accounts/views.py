from rest_framework import status, generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from .serializers import (
    LoginResponseSerializer,
    LoginSerializer,
    MessageSerializer,
    RegisterSerializer,
    UserProfileSerializer,
)


class RegisterView(generics.CreateAPIView):
    """
    POST /api/auth/register/
    Creates a new user account and returns an authentication token.
    Does not require existing authentication.
    """
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @extend_schema(summary="Register a new user account")
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "username": user.username,
                "email": user.email,
                "message": "Registration successful.",
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(generics.GenericAPIView):
    """
    POST /api/auth/login/
    Authenticates a user and returns an API token.
    """
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Login and obtain API token",
        request=LoginSerializer,
        responses={200: LoginResponseSerializer},
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "username": user.username,
            }
        )


class LogoutView(generics.GenericAPIView):
    """
    POST /api/auth/logout/
    Deletes the user's authentication token, effectively logging them out.
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Logout and invalidate current API token",
        request=None,
        responses={200: MessageSerializer},
    )
    def post(self, request):
        try:
            request.user.auth_token.delete()
        except Exception:
            pass
        return Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_200_OK,
        )


class MeView(generics.RetrieveUpdateAPIView):
    """GET /api/auth/me/ Return the current user's profile."""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
