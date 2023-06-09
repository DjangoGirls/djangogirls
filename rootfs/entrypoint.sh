#!/bin/sh -e

echo "Applying database migrations"
./manage.py migrate

echo "Starting application"
./manage.py runserver 0.0.0.0:8000
