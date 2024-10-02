from rest_framework_mongoengine.serializers import DocumentSerializer

from api_pages.models.comment import Comment

class CommentSerializer(DocumentSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'created_at','updated_at']