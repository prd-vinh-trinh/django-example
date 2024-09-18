from django.db import models
from django.utils import timezone
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.hashers import make_password

from api_users.managers.user_manager import UserManager
from core.settings import settings
from api_users.models.role import Role
from base.models.time_stamped import TimeStampedModel

AUTH_PROVIDERS = {'facebook': 'facebook', 'google': 'google', 'twitter': 'twitter', 'email': 'email'}

class User(TimeStampedModel, AbstractBaseUser, PermissionsMixin):
    password = models.CharField(verbose_name="password", max_length=255)
    email = models.EmailField(max_length=255, unique=True, null=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=False)
    roles = models.ManyToManyField(Role, related_name="users", null=True)   
    date_joined = models.DateTimeField(default=timezone.now)
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default=AUTH_PROVIDERS.get('email')
    )

    USERNAME_FIELD = "email"
    objects = UserManager()

    class Meta:
        db_table = "users"

    def __str__(self):
        return str(self.id)
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def set_password(self, raw_password):
        self.password = make_password(password=raw_password, salt=settings.SECRET_KEY)
        self._password = raw_password
        
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
