#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

python manage.py migrate --noinput

python manage.py createsuperuser \
    --noinput \
    --skip-checks \
    --username $DJANGO_SUPERUSER_USERNAME \
    --email $DJANGO_SUPERUSER_EMAIL
    # password for this user must be in $DJANGO_SUPERUSER_PASSWORD

python manage.py initsite

python manage.py collectstatic --noinput


exec "$@"