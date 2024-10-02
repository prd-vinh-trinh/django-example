from rest_framework_mongoengine.serializers import DocumentSerializer

from api_pages.models.page import Page
from api_users.serializers.user import ShortUserSerializer

class PageSerializer(DocumentSerializer):
    author = ShortUserSerializer(required = True, many = False)
    class Meta:
        model = Page
        fields = ['id', 'title', 'author', 'content', 'attached_file','comment','created_at', 'updated_at']

    # def to_representation(self, instance):
        