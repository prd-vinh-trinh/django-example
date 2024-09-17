#!/bin/bash

# Check if the database exists, and create it if it doesn't
echo "Checking if database ${DB_NAME} exists..."
DB_EXISTS=$(mysql -h"${DB_HOST}" -u"${DB_USER}" -p"${DB_PASSWORD}" -e "SHOW DATABASES LIKE '${DB_NAME}';" | grep "${DB_NAME}")

if [ -z "$DB_EXISTS" ]; then
  echo "Database ${DB_NAME} does not exist. Creating..."
  mysql -h"${DB_HOST}" -u"${DB_USER}" -p"${DB_PASSWORD}" -e "CREATE DATABASE ${DB_NAME};"
else
  echo "Database ${DB_NAME} already exists."
fi

echo "Applying database migrations..."
python manage.py makemigrations 
python manage.py migrate

exec "$@"
