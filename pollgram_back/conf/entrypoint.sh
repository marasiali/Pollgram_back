#!/bin/sh
set -e

echo "Waiting for postgres..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py migrate --noinput

python manage.py initsuperuser

python manage.py initsite

python manage.py collectstatic --noinput


exec "$@"