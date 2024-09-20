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
        "retrieve": [
            ["admin:users:view"],
        ],
        "update": [
            ["admin:users:edit"],
        ],
        "destroy": [["admin:users:edit"]],
        "multiple_delele": [["admin:users:edit"]],
        "list": [["admin:users:view"]],
        "change_password": [["users:edit-mine"]],
        "get_self_information": [["users:view-mine"]],
    }

    search_map = {
        "first_name": "icontains",
        "last_name": "icontains",
        "email": "icontains"
    }

    def get_permissions(self):
        if self.action in []:
            return [AllowAny()]
        return [IsAuthenticated()]

    # def retrieve(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance)
    #     return Response(serializer.data)

    @action(methods=["get"], detail=False, url_path="get-self-information")
    def get_self_information(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=HTTP_200_OK)

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
