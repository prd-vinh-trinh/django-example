from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from api_users.models.user import User

from django.utils.translation import gettext as _
from api_users.serializers.user import CreateUserSerializer, UserSerializer


class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(methods=['post'], detail=False, url_path='register')
    def register(self, request):
        data = request.data
        serializer = CreateUserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": _("User registered successfully."),
            }, status=status.HTTP_201_CREATED)
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
