from django.db import models

from api_users.models.user import User
from base.models.time_stamped import TimeStampedModel

status = {'todo', 'inprogress', 'done'}

class Task(TimeStampedModel):
    name = models.CharField()
    status = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    user = models.ForeignKey(User)
    
    class Meta:
        db_table = "tasks"

    def __str__(self):
        return str(self.id)
