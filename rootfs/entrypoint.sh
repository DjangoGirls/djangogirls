#!/bin/sh -e

#echo "Make messages"
#./manage.py makemessages --all

echo "Compile messages"
./manage.py compilemessages

echo "Building static files"
# node_modules lives in a docker volume that may predate package.json changes
npm install --no-audit --no-fund
npm run build:local

echo "Applying database migrations"
./manage.py migrate

echo "Starting application"
./manage.py runserver 0.0.0.0:8000
