#!/bin/bash
set -e

# Uncomment the following lines if you want to wait for the database to start
# echo "Waiting for database to start..."
# until PGPASSWORD=$POSTGRES_PASSWORD psql -h "db" -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
#     echo >&2 "Postgres is unavailable - sleeping"
#     sleep 1
# done
# echo "Postgres is up - running migrations...."

# Run migrations
python manage.py makemigrations
python manage.py makemigrations UserManagement
python manage.py migrate UserManagement
python manage.py makemigrations blog orders
python manage.py migrate
echo "Migrations complete"

# Create a background process for gunicorn server
gunicorn PortfolioBackend.wsgi:application --bind 0.0.0.0:8000 --workers 2 --threads 2

# Store the background process ID
gunicorn_pid=$!

# Uncomment the following line if you want to run the Django server using 'python manage.py runserver'
# python manage.py runserver

# Wait for the gunicorn server to complete before exiting the script
wait $gunicorn_pid
