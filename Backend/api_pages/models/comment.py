import mongoengine as me
from datetime import datetime

class Comment(me.EmbeddedDocument):
    child_comments = me.EmbeddedDocumentListField("Comment")
    content = me.StringField(required=True)
    created_at = me.DateTimeField(default=datetime.now)

    class Meta : 
        _use_db = 'nonrel'
        ordering = ['-updated_at'],

    def __str__(self):
        return f"Comment by {self.author} on {self.page.title}"

    def get_replies(self):
        return Comment.objects(parent_comment=self)
