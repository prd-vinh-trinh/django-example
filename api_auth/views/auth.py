from django.core.cache import cache

from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from api_auth.services.auth import AuthService
from api_users.models.user import User

from django.utils.translation import gettext as _
from api_users.serializers.user import CreateUserSerializer, UserSerializer


class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(methods=['post'], detail=False, url_path='register')
    def register(self, request):
        email = request.data.get("email")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        password = request.data.get("password")
        data = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
        }
        serializer = CreateUserSerializer(data=data)

        if serializer.is_valid():
            try:
                user = serializer.save()
                token = AuthService.verify_user_email(
                    email, first_name, last_name, role_ids=None)
                cache.set(key=f"verify_register_token",
                          value=token,
                          timeout=60 * 15,)
                print(cache.get(f"verify_{email}"))
                return Response({
                    "message": _("User registered successfully."),
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                serializer.delete(user)
                return Response({"Error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='login')
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"detail": _("Email or Username and password are required.")}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=username)

            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "profile": UserSerializer(user).data
                }, status=status.HTTP_200_OK)
            return Response({"Error": _("Invalid credentials.")}, status=status.HTTP_401_UNAUTHORIZED)

        except User.DoesNotExist:
            return Response({"Error": _("User not found.")}, status=status.HTTP_404_NOT_FOUND)
