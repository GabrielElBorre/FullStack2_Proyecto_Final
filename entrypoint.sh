#!/bin/sh
set -e

echo "Esperando base de datos..."
for i in $(seq 1 30); do
    if python manage.py check --database default 2>/dev/null; then
        break
    fi
    sleep 2
done

echo "Ejecutando migraciones..."
python manage.py migrate --noinput

echo "Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "Preparando carpeta media..."
mkdir -p /app/media/campaigns
chmod -R 755 /app/media

echo "Cargando usuarios de prueba..."
python manage.py seed_users || true
python manage.py seed_campaigns || true

if [ "$DEBUG" = "True" ] || [ "$DEBUG" = "true" ]; then
    exec python manage.py runserver 0.0.0.0:8000
else
    exec gunicorn django_project.wsgi:application --bind 0.0.0.0:8000 --workers 3
fi
