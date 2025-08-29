#!/bin/sh
set -e

echo "Running database migrations..."
echo "Making migrations (if needed)..."
python src/manage.py makemigrations --noinput || true
python src/manage.py migrate --noinput

echo "Collecting static files..."
python src/manage.py collectstatic --noinput

echo "Starting server..."
if [ "$#" -eq 0 ]; then
	# No command provided by Docker; start the default Django development server
	echo "No command passed to entrypoint, launching default runserver"
	exec python src/manage.py runserver 0.0.0.0:8000
else
	exec "$@"
fi
