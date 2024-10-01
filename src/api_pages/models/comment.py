import mongoengine as me
from datetime import datetime

from api_pages.models.page import Page

class Comment(me.Document):
    page = me.ReferenceField(Page, reverse_delete_rule=me.CASCADE)
    parent_comment = me.ReferenceField('self', null=True, blank=True, reverse_delete_rule=me.CASCADE)
    content = me.StringField(required=True)
    created_at = me.DateTimeField(default=datetime.now)
    author = me.StringField(max_length=100)

    meta = {
        'collection': 'comments',
        'ordering': ['-created_at'],
    }

    def __str__(self):
        return f"Comment by {self.author} on {self.page.title}"

    def get_replies(self):
        return Comment.objects(parent_comment=self)
