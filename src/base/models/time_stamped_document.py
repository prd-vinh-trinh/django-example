import uuid
import mongoengine as me

from django.utils.timezone import now

class BaseDocumentModel(me.Document):
    created_at = me.DateTimeField(default=now)
    updated_at = me.DateTimeField()

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.updated_at:
            self.created_at = now()
            self.updated_at = now()
        if not self.created_at == self.updated_at:
            self.updated_at = now()
        super().save(*args, **kwargs)

