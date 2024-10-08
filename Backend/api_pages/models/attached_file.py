import mongoengine as me

class AttachedFile(me.EmbeddedDocument):
    file_path = me.StringField(require=True)
    
    meta = {
        'allow_inheritance' : 'True',
    }
    
    class Meta : 
        _use_db = 'nonrel'
        ordering= ['-updated_at'],


