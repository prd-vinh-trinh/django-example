from django.db import models
from django.utils.timezone import now

from base.models.time_stamped import TimeStampedModel

class User(AbstractBaseUser,PermissionMixin,TimeStampedModel):


    class Meta:

