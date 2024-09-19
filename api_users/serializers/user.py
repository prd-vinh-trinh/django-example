from rest_framework import serializers

from api_users.models.user import User
from api_users.models.role import Role
from api_users.serializers.role import RoleSerializer


class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(required=False, many=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "roles"
        ]
        depth = 1


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "password", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        try:
            user = User.objects.create(**validated_data)
            role, _ = Role.objects.get_or_create(
                name="User",
                description="User role",
                scope="__all__"
            )
            user.roles.add(role)
            user.set_password(validated_data["password"])
            user.is_superuser = False
            user.save()
            return user
        except Exception as e:
            # Call delete method to rollback the user creation
            self.delete(user)
            raise e  # Re-raise the exception to propagate it further

    def delete(self, instance):
        if instance and instance.pk:
            instance.delete()


class ShortUserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(required=False, many=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "role"
        ]
        depth = 1
