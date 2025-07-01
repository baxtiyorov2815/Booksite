#!/bin/sh

echo "Waiting for db..."
while ! nc -z db 5432; do
  sleep 1
done


echo "Running migrations..."
python manage.py migrate

echo "Running makemigrations..."
python manage.py makemigrations

echo "Collecting static files..."
python manage.py collectstatic --noinput
