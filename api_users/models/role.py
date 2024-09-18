from django.db import models

# Create your models here.
class Role(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, unique=True)
    description = models.TextField(default="", null=True, blank=True)
    scope = models.TextField(default="", null=True, blank=True)
    last_modified_by = models.CharField(max_length=255, null=True, blank=True, default="")

    def __str__(self):
        return self.name

    class Meta:
        db_table = "roles"
        
    @property
    def scopes(self):
        from oauth2_provider.scopes import get_scopes_backend
        all_scopes = get_scopes_backend().get_all_scopes()
        if self.scope == "__all__":
            return {name: desc for name, desc in all_scopes.items()}
        role_scopes = self.scope.split()
        return {name: desc for name, desc in all_scopes.items() if name in role_scopes}

    