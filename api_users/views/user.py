from django.forms import ValidationError
from api_users.models.user import User
from api_users.serializers import UserSerializer
from base.services.verification import Verification
from base.views.base import BaseViewSet
from django.contrib.auth import password_validation
from django.utils.translation import gettext as _
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_nested_forms.utils import NestedForm
from rest_framework.permissions import AllowAny, IsAuthenticated


from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_500_INTERNAL_SERVER_ERROR,
)


class UserViewSet(BaseViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    required_alternate_scopes = {
        "create": [["admin:users:edit"]],
        "invite": [["admin:users:edit"],],
        "retrieve": [
            ["admin:users:view"],
            ["admin:users:edit"],
        ],
        "update": [
            ["users:edit-mine"],
            ["admin:users:edit"],
        ],
        "destroy": [["admin:users:edit"]],
        "multiple_delele": [["admin:users:edit"]],
        "list": [["admin:users:view"], ["admin:users:edit"]],
        "change_password": [["users:edit-mine"]],
        "import_data": [["admin:users:edit"]],
        "get_self_information": [["users:view-mine"]],
    }
    search_map = {
        "first_name": "icontains",
        "last_name": "icontains",
        "email": "icontains"
    }

    def get_permissions(self):
        """Returns the permission based on the type of action"""
        if self.action in ["get_name_by_id"]:
            return [AllowAny()]
        return [IsAuthenticated()]

    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to customize JSON response if needed"""
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=["get"], detail=False, url_path="get-self-information")
    def get_self_information(self, request, *args, **kwargs):
        user = request.user  # Retrieves the currently authenticated user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=HTTP_200_OK)

    @action(methods=["get"], detail=False, url_path="get-name")
    def get_name_by_id(self, request, *args, **kwargs):
        user_id = request.query_params.get('id')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=HTTP_404_NOT_FOUND)

        # Use the serializer to get the user data
        serializer = self.get_serializer(user)
        user_data = {
            "id": serializer.data['id'],
            "first_name": serializer.data['first_name'],
            "last_name": serializer.data['last_name']
        }
        return Response(user_data, status=HTTP_200_OK)

    @action(methods=["put"], detail=True)
    def change_password(self, request, *args, **kwargs):
        data = request.data
        user = self.get_object()
        password = data.get("old_password")
        password1 = data.get("new_password1")
        password2 = data.get("new_password2")
        if password1 and password2 and password1 != password2:
            return Response(
                {"message": _("The passwords are mismatch.")},
                status=HTTP_406_NOT_ACCEPTABLE,
            )
        try:
            password_validation.validate_password(password, user)
        except ValidationError as error:
            return Response(
                {"message": _("The passwords is invalid format")},
                status=HTTP_406_NOT_ACCEPTABLE,
            )

        try:
            user.set_password(password1)
            self.perform_update(user)
        except Exception as e:
            print(e)
            return Response(
                {"message": _("There is an error occur.")},
                status=HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response({"message": _("The passwword have been updated.")})

    @action(methods=["get"], detail=True, url_path="invite")
    def invite(self, request, *args, **kwargs):
        email = request.data.get("email")
        user = self.get_object()
        user.send_invitation_email(email)

        return Response({"message": _("The passwword have been updated.")})

    @action(detail=False, methods=["post"], url_path="verify_invitation", permission_classes=[AllowAny], authentication_classes=[])
    def verify_invitation(self, request, *args, **kwargs):
        content_type = request.content_type
        data = request.data.copy()
        if content_type is not None and 'form-data' in content_type:
            form = NestedForm(request.data)
            if form.is_nested():
                data = form.data
        token = data.get('token')
        if token is not None:
            del data['token']

        try:
            token_payload = Verification.decode_token(token)
            token_email = token_payload.get('email')
            print('token_email: ', token_email)
            user = User.objects.get(email=token_email)
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
