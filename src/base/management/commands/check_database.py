import os
import MySQLdb
from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.conf import settings

class Command(BaseCommand):
    help = "Check if the database exists, and create it if not."

    def handle(self, *args, **options):
        db_name = os.getenv('DB_NAME')
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT', 3306)

        try:
            conn = connections['default']
            conn.ensure_connection()
            self.stdout.write(self.style.SUCCESS(f"Database '{db_name}' exists."))
        except Exception:
            self.stdout.write(self.style.WARNING(f"Database '{db_name}' does not exist. Attempting to create it..."))

            try:
                connection = MySQLdb.connect(
                    host=db_host,
                    user=db_user,
                    passwd=db_password,
                    port=int(db_port)
                )
                connection.autocommit(True)
                cursor = connection.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
                cursor.close()
                self.stdout.write(self.style.SUCCESS(f"Database '{db_name}' created successfully."))
            except MySQLdb.Error as err:
                raise CommandError(f"Error creating database: {err}")
