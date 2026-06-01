#!/bin/sh
# Script de despliegue rápido en una instancia OCI con Docker instalado.
set -e

if [ ! -f .env ]; then
    echo "Copia .env.example a .env y configura SECRET_KEY, ALLOWED_HOSTS y EMAIL_*"
    exit 1
fi

docker compose pull
docker compose up -d --build

echo "Despliegue iniciado. Accede a http://<IP_PUBLICA>:8000"
