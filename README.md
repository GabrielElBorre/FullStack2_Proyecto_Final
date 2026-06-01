# Plataforma de Donaciones

Proyecto académico en **Django 5.x** y **Python 3.12** con **PostgreSQL**, **Docker** y despliegue preparado para **Oracle Cloud Infrastructure (OCI)**.

## Captura de pantalla

> Sustituye esta sección con una captura de la aplicación en producción (lista de campañas con barra de progreso).

![Captura de la plataforma](docs/screenshot.png)

## Credenciales de prueba

| Rol | Email | Contraseña |
|-----|-------|------------|
| Superusuario / Admin | `admin@donaciones.com` | `admin123` |
| Usuario donante | `usuario@test.com` | `testpass123` |

El admin puede crear/editar/eliminar campañas. El usuario normal puede registrarse, donar y ver **solo sus donaciones** en «Mis donaciones».

## Requisitos cumplidos (rúbrica)

- Django 5.x + Python 3.12 (Dockerfile `python:3.12-slim`)
- PostgreSQL (sin SQLite)
- Variables con `django-environ` (`SECRET_KEY`, `DEBUG`, `DATABASE_URL`, `EMAIL_*`)
- `CustomUser` con login por email
- Modelos `Campaign` y `Donation`
- CBV, URLs amigables, Bootstrap 5
- Autenticación completa (registro, login, logout, cambio y restablecimiento de contraseña)
- CRUD de campañas con permisos por rol (`donante`, `creador`, `admin`)
- Búsqueda de campañas + barra de progreso visual
- 5+ pruebas unitarias
- Docker Compose (`web` + `db`)

## Estructura

```
plataforma_donaciones/
├── apps/accounts/      # Usuario personalizado y autenticación
├── apps/campaigns/     # Campañas (CRUD)
├── apps/donations/     # Donaciones
├── django_project/     # settings, urls, wsgi
├── templates/          # base.html, account/, campaigns/, donations/
├── static/             # CSS
├── media/              # Imágenes de campañas
├── Dockerfile
└── docker-compose.yml
```

## Inicio rápido con Docker

```bash
cd plataforma_donaciones
cp .env.example .env
docker compose up --build
```

Abre: http://localhost:8000

## Desarrollo local (sin Docker)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt
cp .env.example .env
# Ajusta DATABASE_URL a tu PostgreSQL local
python manage.py migrate
python manage.py seed_users
python manage.py runserver
```

## Pruebas

```bash
docker compose exec web python manage.py test
```

## Despliegue en OCI

1. Crea una instancia Compute (Ubuntu) con IP pública.
2. Instala Docker y Docker Compose.
3. Clona el repositorio y configura `.env` en producción:

```env
DEBUG=False
SECRET_KEY=<clave-larga-aleatoria>
DATABASE_URL=postgres://usuario:clave@db:5432/donaciones
ALLOWED_HOSTS=tu-ip-publica,tu-dominio.com
CSRF_TRUSTED_ORIGINS=https://tu-dominio.com
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=...
EMAIL_PORT=587
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
```

4. Abre el puerto **8000** (o 80 con proxy) en el Security List.
5. Ejecuta:

```bash
docker compose up -d --build
```

6. Accede desde el navegador: `http://<IP_PUBLICA>:8000`

## Roles de usuario

| Rol | Permisos |
|-----|----------|
| `donante` | Donar, ver sus donaciones |
| `creador` | Crear y editar sus campañas |
| `admin` / `is_staff` | Todo + eliminar campañas |

Asigna el rol desde el panel `/admin/` o al crear usuarios.

## Comandos útiles

```bash
python manage.py seed_users      # Usuarios de prueba
python manage.py seed_campaigns  # Campañas de demostración
python manage.py test            # Pruebas unitarias
```

## Git

Historial con commits significativos: configuración inicial, datos demo, despliegue OCI, media y documentación.

## Autor

Proyecto académico — Plataforma de Donaciones.
