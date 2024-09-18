import json
from django.http import HttpResponse
from oauth2_provider.signals import app_authorized
from oauth2_provider.models import get_access_token_model
from oauthlib.oauth2.rfc6749.utils import list_to_scope
from oauth2_provider.views.mixins import OAuthLibMixin
from rest_framework.response import Response
from django.utils.translation import gettext as _
from api_users.serializers import CreateUserSerializer

from api_users.models.user import User
from oauth.services.user import UserService
from base.services.verification import Verification
from core.settings.base import (
    DEFAULT_CLIENT_ID,
    DEFAULT_CLIENT_SECRET,
)
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_406_NOT_ACCEPTABLE,
)

from rest_framework.viewsets import ViewSet
from rest_framework.decorators import action
from django.contrib.auth import authenticate


from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model



OAuthUser = get_user_model()
AccessToken = get_access_token_model()

class Oauth2ViewSet(OAuthLibMixin, ViewSet):
    """
    The endpoints for login, refresh token and logout
    """

    required_alternate_scopes = ["read", "write"]  # Define your required scopes here

    def get_permissions(self):
        """Returns the permission based on the type of action"""
        if self.action in ["login", "register", "refreshToken","verify" ,"loginWithGoogle"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(
        detail=False,
        methods=["post"],
        url_path="register",
        permission_classes=[AllowAny],
        authentication_classes=[],
    )
    def register(self, request):
        """
        Registers user to the server. Input should be in the format:
        {"username": "username", "password": "1234abcd"}
        """
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
        # Put the data from the request into the serializer
        serializer = CreateUserSerializer(data=data)
        # Validate the data
        if serializer.is_valid():
            try:
                user = serializer.save()
                UserService.verify_user_email(email, first_name, last_name, role_ids=None)
                return Response(serializer.data, status=HTTP_201_CREATED)
            except Exception as e:
                serializer.delete(user)
                return Response({"error": str(e)}, status=HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=["post"], url_path="verify", permission_classes=[AllowAny], authentication_classes=[])
    def verify(self, request, *args, **kwargs):
        data = request.data.copy()
        token = data.get('token')
        if token is not None:
            del data['token']

        try:
            token_payload = Verification.decode_token(token)
            token_email = token_payload.get('email')
            print('token_email: ', token_email)
            user = User.objects.get(email=token_email)
            print(user)
            if user is None:
                return Response(
                    {"error": _("Invalid token")},
                    status=HTTP_406_NOT_ACCEPTABLE,
                )
            if user.is_active == False:
                user.is_active = True
                user.save()
            else:
                return Response(
                    {"error": _("User already activated")},
                    status=HTTP_400_BAD_REQUEST,
                )
            return Response(
                {"message": _("User activated successfully")},
                status=HTTP_200_OK,
            )

        except Exception as e:
            return Response(
                {"error": _("Invalid token")},
                status=HTTP_406_NOT_ACCEPTABLE,
            )
            
    @action(
        detail=False,
        methods=["post"],
        url_path="login",
        permission_classes=[AllowAny],
        authentication_classes=[],
    )
    def login(self, request, pk=None):
        try:
            user_name = request.POST.get("username")
            password = request.POST.get("password")
            if not user_name or not password:
                return Response(
                    {"error": _("Username and password are required.")},
                    status=HTTP_404_NOT_FOUND,
                )
            user = authenticate(username=user_name, password=password)
            if user is None:
                return Response(
                    {"error": _("Invalid username or password.")},
                    status=HTTP_404_NOT_FOUND,
                )

        except OAuthUser.DoesNotExist:
            return Response(
                {"error": _("The user does not exist.")},
                status=HTTP_404_NOT_FOUND,
            )
        scopes = set()
        for role in user.roles.all():
            scopes = scopes.union(set(role.scopes.keys()))
        request.POST._mutable = True
        request.POST.update(
            {
                "grant_type": "password",
                "client_type": "confidential",
                "client_id": DEFAULT_CLIENT_ID,
                "client_secret": DEFAULT_CLIENT_SECRET,
                "scope": list_to_scope(scopes),
            }
        )
        url, headers, body, status = self.create_token_response(request)

        if status == 200:
            access_token = json.loads(body).get("access_token")
            if access_token is not None:
                token = AccessToken.objects.get(token=access_token)
                app_authorized.send(sender=self, request=request, token=token)
        response = HttpResponse(content=body, status=status)

        for k, v in headers.items():
            response[k] = v
        return response

    @action(
        detail=False,
        methods=["post"],
        url_path="refresh-token",
        permission_classes=[AllowAny],
        authentication_classes=[],  
    )
    def refreshToken(self, request):
        request.POST._mutable = True
        refresh_token = request.POST.get("refresh_token")
        if not refresh_token or refresh_token == "null":
            return Response(
                {"error": _("Invalid token")},
                status=HTTP_406_NOT_ACCEPTABLE,
            )
        request.POST.update(
            {
                "grant_type": "refresh_token",
                "client_id": DEFAULT_CLIENT_ID,
                "client_secret": DEFAULT_CLIENT_SECRET,
                "refresh_token": refresh_token,
            }
        )
        url, headers, body, status = self.create_token_response(request)
        if status == 200:
            access_token = json.loads(body).get("access_token")
            if access_token is not None:
                token = AccessToken.objects.get(token=access_token)
                app_authorized.send(sender=self, request=request, token=token)
        response = HttpResponse(content=body, status=status)

        for k, v in headers.items():
            response[k] = v
        return response

    @action(detail=False, methods=["post"], url_path="logout")
    def logout(self, request, pk=None):
        refresh_token = request.POST.get("refresh_token")
        access_token = request.POST.get("access_token")
        request.POST._mutable = True
        # revoke refresh_token first, to make user can not renew access_token
        request.POST.update(
            {
                "client_id": DEFAULT_CLIENT_ID,
                "client_secret": DEFAULT_CLIENT_SECRET,
                "token_type_hint": "refresh_token",
                "token": refresh_token,
            }
        )
        url, headers, body, status = self.create_revocation_response(request)
        if status != HTTP_200_OK:
            return HttpResponse(
                content={"error": "can not revoke refresh_token"},
                status=HTTP_400_BAD_REQUEST,
            )

        # revoke access_token
        request.POST.update(
            {
                "token_type_hint": "access_token",
                "token": access_token,
            }
        )
        url, headers, body, status = self.create_revocation_response(request)
        if status != HTTP_200_OK:
            return HttpResponse(
                content={"error": "can not revoke access_token"},
                status=HTTP_400_BAD_REQUEST,
            )

        return Response({"message": "logout success!"}, status=HTTP_200_OK)