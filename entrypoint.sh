#!/bin/sh
set -e

echo "Running database migrations..."
python src/manage.py migrate --noinput

echo "Collecting static files..."
python src/manage.py collectstatic --noinput

echo "Starting server..."
exec "$@"
