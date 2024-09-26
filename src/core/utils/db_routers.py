class DatabaseRouter:
    """
    A router to control if database should use
    relationship database or non relationship database
    """

    nosql_models = {'log'}

    def db_for_read(self, model, **_hints):
        if model._meta.model_name in self.nosql_models:
            return 'nosql'
        return 'default'

    def db_for_write(self, model, **_hints):
        if model._meta.model_name in self.nosql_models:
            return 'nosql'
        return 'default'

    def allow_migrate(self, _db, _app_label, model_name=None, **_hints):
        if _db == 'nosql' or model_name in self.nosql_models:
            return False
        return True
