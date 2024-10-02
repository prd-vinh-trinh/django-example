from rest_framework_mongoengine.serializers import DocumentSerializer

from api_pages.models.page import Page

class PageSerializer(DocumentSerializer):
    class Meta:
        model = Page
        fields = ['id', 'title', 'author', 'content', 'attached_file','comment','created_at', 'updated_at']
