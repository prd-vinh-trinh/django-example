import mongoengine as me

from base.models.time_stamped_document import BaseDocumentModel
from api_pages.models.comment import Comment
from api_pages.models.attached_file import AttachedFile

class Page(BaseDocumentModel):
    title = me.StringField(max_length=200, required=True)
    author = me.StringField(require=True)
    content = me.StringField(required=True)
    attached_file = me.EmbeddedDocumentListField(AttachedFile)
    comment = me.EmbeddedDocumentListField(Comment)

    class Meta : 
        _use_db = 'nonrel'
        collection = 'pages',
        ordering= ['-updated_at'],

    def __str__(self):
        return self.title