class DatabaseRouter:
    """
    A router to control database operations for users, tasks, and NoSQL.
    """

    user_models = {'user'}
    task_models = {'task'}
    nosql_models = {}

    def db_for_read(self, model, **_hints):
        """
        Direct read operations to the appropriate database.
        """
        if model._meta.model_name in self.user_models:
            return 'default'
        elif model._meta.model_name in self.task_models:
            return 'db_task'
        elif model._meta.model_name in self.nosql_models:
            return 'nosql'
        return 'default'

    def db_for_write(self, model, **_hints):
        """
        Direct write operations to the appropriate database.
        """
        if model._meta.model_name in self.user_models:
            return 'default'
        elif model._meta.model_name in self.task_models:
            return 'db_task'
        elif model._meta.model_name in self.nosql_models:
            return 'nosql'
        return 'default'

    def allow_migrate(self, _db, _app_label, model_name=None, **_hints):
        """
        Prevent migrations on certain databases.
        """
        if _db == 'nosql' or (model_name in self.nosql_models):
            return False
        elif _db == 'default' and model_name not in self.user_models:
            return False
        elif _db == 'db_task' and model_name not in self.task_models:
            return False
        return True
