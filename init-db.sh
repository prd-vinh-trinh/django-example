#!/bin/bash

echo "Starting database initialization..."
while ! mysqladmin ping -h"localhost" --silent; do
    sleep 1
done

mysql -u root -p"${DB_PASSWORD}" -e "CREATE DATABASE IF NOT EXISTS ${DB_NAME_01};"
mysql -u root -p"${DB_PASSWORD}" -e "CREATE DATABASE IF NOT EXISTS ${DB_NAME_02};"

mysql -u root -p"${DB_PASSWORD}" -e "CREATE USER IF NOT EXISTS '${DB_USER}'@'%' IDENTIFIED BY '${DB_PASSWORD}';"
mysql -u root -p"${DB_PASSWORD}" -e "GRANT ALL PRIVILEGES ON ${DB_NAME_01}.* TO '${DB_USER}'@'%';"
mysql -u root -p"${DB_PASSWORD}" -e "GRANT ALL PRIVILEGES ON ${DB_NAME_02}.* TO '${DB_USER}'@'%';"
mysql -u root -p"${DB_PASSWORD}" -e "FLUSH PRIVILEGES;"
echo "Finished database initialization."