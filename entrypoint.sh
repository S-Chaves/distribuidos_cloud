#!/bin/sh

# El script falla si un comando falla.
set -e

echo "Corriendo migraciones de la base de datos..."
poetry run flask db upgrade

echo "Sembrando la base de datos..."
poetry run flask seed-db

echo "Iniciando el servidor Gunicorn..."
exec gunicorn wsgi:app -b 0.0.0.0:${PORT:-8000}
