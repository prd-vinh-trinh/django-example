from ..models.role import Role
from rest_framework import serializers


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            "id",
            "name",
            "description",
            "scope",
            "last_modified_by",
        ]
        extra_kwargs = {
            "name": {"required": False},
            "description": {"required": False},
            "scope": {"required": False},
            "last_modified_by": {"required": False},
        }


class ShortRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = [
            "id",
            "name",
            "description",
        ]
        extra_kwargs = {
            "name": {"required": False},
            "description": {"required": False},
        }