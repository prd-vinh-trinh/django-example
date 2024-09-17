#!/bin/bash
echo "Check if the database exists and create it if it doesn't"
python manage.py check_database

echo "Applying database migrations..."
python manage.py makemigrations 
python manage.py migrate

exec "$@"
