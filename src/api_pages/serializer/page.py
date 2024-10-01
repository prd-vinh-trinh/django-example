from rest_framework_mongoengine import DocumentSerializer

from api_pages.models.page import Page

class PageSerializer(DocumentSerializer):
    class Meta:
        model = Page
        fields = ['id', 'title', 'author', 'content', 'attached_file', 'created_at']
