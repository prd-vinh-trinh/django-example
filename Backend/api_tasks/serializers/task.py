from asyncio import Task
from rest_framework import serializers

from api_users.serializers.user import ShortUserSerializer

class TaskSerializer(serializers.ModelSerializer):

    user = ShortUserSerializer(required = True, multi = False)
    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "status",
            "start_date",
            "end_date",
            "user"
        ]
        depth = 1



class ShortTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [
            "id",
            "name",
            "status",
            "start_date",
            "end_date",
        ]