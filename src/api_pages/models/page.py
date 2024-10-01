import mongoengine as me
from datetime import datetime

from api_pages.models.attached_file import AttachedFile
from base.models.time_stamped_document import BaseDocumentModel

class Page(BaseDocumentModel):
    title = me.StringField(max_length=200, required=True)
    author = me.StringField(require=True)
    content = me.StringField(required=True)
    attached_file = me.EmbeddedDocumentField(AttachedFile)

    meta = {
        'collection': 'pages',
        'ordering': ['-created_at'],
    }

    def __str__(self):
        return self.title