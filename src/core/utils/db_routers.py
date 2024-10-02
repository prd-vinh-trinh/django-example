class DatabaseRouter:
    """
    A router to control if the database should use
    the relational database, non-relational database, or management database.
    """

    nosql_models = {'log'}
    management_models = {'task'}

    def db_for_read(self, model, **_hints):
        """
        Direct reading operations to the appropriate database.
        """
        if model._meta.model_name in self.nosql_models:
            return 'nosql'
        elif model._meta.model_name in self.management_models:
            return 'management'
        return 'default'

    def db_for_write(self, model, **_hints):
        """
        Direct writing operations to the appropriate database.
        """
        if model._meta.model_name in self.nosql_models:
            return 'nosql'
        elif model._meta.model_name in self.management_models:
            return 'management'
        return 'default'

    def allow_migrate(self, _db, _app_label, model_name=None, **_hints):
        """
        Prevent migration on certain databases.
        """
        if _db == 'nosql' or model_name in self.nosql_models:
            # No migrations for the NoSQL database
            return False
        elif _db == 'management' and model_name not in self.management_models:
            # Allow migrations only for management-related models in the management database
            return False
        return True
