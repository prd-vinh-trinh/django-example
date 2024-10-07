import os
from django.core.management.base import BaseCommand, CommandError
from django.db import connections
import MySQLdb


class Command(BaseCommand):
    help = "Check if the databases exist, and create them if not."

    def handle(self, *args, **options):
        db_name_default = os.getenv('DB_NAME_DEFAULT')
        db_name_01 = os.getenv('DB_NAME_01')
        db_name_02 = os.getenv('DB_NAME_02')
        db_user = os.getenv('DB_USER')
        db_password = os.getenv('DB_PASSWORD')
        db_host = os.getenv('DB_HOST')
        db_port = os.getenv('DB_PORT', 3306)

        try:
            conn = connections['default']
            conn.ensure_connection()
            self.stdout.write(self.style.SUCCESS(
                f"Database '{db_name_default}' exists."))
            self.stdout.write(self.style.SUCCESS(
                f"Database '{db_name_01}' exists."))
            self.stdout.write(self.style.SUCCESS(
                f"Database '{db_name_02}' exists."))
        except Exception:
            self.stdout.write(self.style.WARNING(f"Checking databases..."))


            try:
                connection = MySQLdb.connect(
                    host=db_host,
                    user=db_user,
                    passwd=db_password,
                    port=int(db_port)
                )
                connection.autocommit(True)
                cursor = connection.cursor()

                # Tạo cơ sở dữ liệu nếu không tồn tại
                for db_name in [db_name_default, db_name_01, db_name_02]:
                    cursor.execute(
                        f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")
                    self.stdout.write(self.style.SUCCESS(
                        f"Database '{db_name}' created successfully."))

                cursor.close()
            except MySQLdb.Error as err:
                raise CommandError(f"Error creating database: {err}")
            finally:
                if 'connection' in locals():
                    connection.close()
