import mongoengine as me
from datetime import datetime

from api_pages.models.page import Page

class AttachedFile(me.EmbeddedDocument):
    file_path = me.StringField(require=True)
    created_at = me.DateTimeField(default=datetime.now)

    meta = {
        'collection': 'comments',
        'ordering': ['-created_at'],
    }


