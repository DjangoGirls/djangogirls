#!/bin/sh -e

#echo "Make messages"
#./manage.py makemessages --all

if [ "$NODE_ENV" = "development" ]; then
    echo "Compiling static files"
    gulp watch
fi

echo "Compile messages"
./manage.py compilemessages

echo "Applying database migrations"
./manage.py migrate

echo "Starting application"
./manage.py runserver 0.0.0.0:8000
