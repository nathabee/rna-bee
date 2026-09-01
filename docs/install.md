# Installation

This document describes a fresh installation of RNA Bee from a Git clone.

VPS-specific Apache and HTTPS configuration is documented separately in `install-vps.md`.

## Prerequisites

The target system needs:

- Git
- Docker Engine
- Docker Compose v2 (`docker compose`)
- a user allowed to run Docker
- network access to pull Docker images and clone the repository

For the production VPS, Apache and HTTPS are configured outside the Docker stack. See `docs/install-vps.md`.

## Clone the repository

Clone RNA Bee and enter the project directory:

```bash
cd ~

git clone git@github.com:nathabee/rna-bee.git

cd rna-bee
```

For an existing checkout:

```bash
cd ~/rna-bee

git pull
```

The deployment checkout should normally stay clean. Development changes should be committed locally, pushed to GitHub, and pulled on the target system.

## Configure the environment

Create the local environment file:

```bash
cp .env.example .env
```

Edit it:

```bash
nano .env
```

At minimum, review and replace the example values for:

```dotenv
PUBLIC_HOST=rna.nathabee.de

DJANGO_ALLOWED_HOSTS=rna.nathabee.de,localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=https://rna.nathabee.de
DJANGO_CORS_ALLOWED_ORIGINS=https://rna.nathabee.de

WORDPRESS_HOST_PORT=8110
DJANGO_HOST_PORT=8111

DJANGO_SECRET_KEY=YOURPASSWORD

POSTGRES_DB=rnabee
POSTGRES_USER=rnabee
POSTGRES_PASSWORD=YOURPASSWORD

MARIADB_DATABASE=wordpress
MARIADB_USER=wordpress
MARIADB_PASSWORD=YOURPASSWORD
MARIADB_ROOT_PASSWORD=YOURPASSWORD

REDIS_URL=redis://redis:6379/0
SIMULATION_RESULTS_DIR=/data/results

WP_URL=https://rna.nathabee.de
WP_TITLE=RNA Bee
WP_ADMIN_USER=rnabee
WP_ADMIN_PASSWORD=YOURPASSWORD
WP_ADMIN_EMAIL=admin@example.com
```

Do not commit `.env`.

Validate the Compose configuration before starting:

```bash
docker compose config
```

## Build the application images

Build the Django and Celery images:

```bash
docker compose build
```

A no-cache build is only needed when explicitly troubleshooting cached image layers:

```bash
docker compose build --no-cache
```

## Start the Docker stack

Start the services:

```bash
docker compose up -d
```

Check their state:

```bash
docker compose ps
```

The main services are:

```text
wordpress
wordpress-db
django
celery-worker
postgres
redis
```

`wp-cli` is a tool service and is started only when required.

Wait until the database health checks report healthy before bootstrapping WordPress.

## Bootstrap WordPress

RNA Bee does not require a manual WordPress installation through the browser.

Run the WP-CLI bootstrap:

```bash
docker compose run --rm wp-cli /bootstrap/bootstrap.sh
```

The bootstrap is designed to be idempotent. It can be run again without creating duplicate seed pages.

It currently performs the following tasks:

- installs WordPress when it is not already installed
- configures the WordPress site
- sets the permalink structure
- ensures Twenty Twenty-Five is installed
- activates the `rna-bee` child theme
- activates the `rna-bee` plugin
- removes the default `Hello world!` post and `Sample Page`
- creates `Home`, `About RNA Bee`, and `Explore`
- assigns the child theme's `page-no-title` template to the seeded pages
- sets `Home` as the static front page

The theme and plugin are bind-mounted from the Git checkout:

```text
wordpress/themes/rna-bee
    -> /var/www/html/wp-content/themes/rna-bee

wordpress/plugins/rna-bee
    -> /var/www/html/wp-content/plugins/rna-bee
```

They therefore remain version-controlled independently of the WordPress Docker volume.

## Verify the installation

Check all containers:

```bash
docker compose ps
```

Test WordPress locally on the host:

```bash
curl -I http://127.0.0.1:8110/
```

Test the Django health endpoint:

```bash
curl http://127.0.0.1:8111/api/health/
```

Expected Django response:

```json
{"status":"ok","service":"rna-bee-api"}
```

Check the active WordPress theme:

```bash
docker compose run --rm wp-cli -c \
'wp theme list --status=active'
```

Check active plugins:

```bash
docker compose run --rm wp-cli -c \
'wp plugin list --status=active'
```

Confirm the application files are visible inside WordPress:

```bash
docker compose exec wordpress \
  ls -la /var/www/html/wp-content/themes/rna-bee

docker compose exec wordpress \
  ls -la /var/www/html/wp-content/plugins/rna-bee
```

For a production VPS, continue with the Apache and HTTPS checks in `docs/install-vps.md`.

## Normal start after installation

Once WordPress has been bootstrapped, a normal start only requires:

```bash
docker compose up -d
```

The WordPress bootstrap does not need to run after every container restart.

Run it again when WordPress bootstrap behavior or seed configuration has changed:

```bash
docker compose run --rm wp-cli /bootstrap/bootstrap.sh
```

## Logs

Show recent logs for all services:

```bash
docker compose logs --tail=100
```

Follow logs:

```bash
docker compose logs -f
```

Examples for individual services:

```bash
docker compose logs wordpress --tail=100
docker compose logs django --tail=100
docker compose logs celery-worker --tail=100
```

## Reinstallation and service reset

Fresh-install and per-service reset procedures are intentionally kept out of this document.

They belong in dedicated operational documentation so that the normal installation path stays short and safe.

Do not use `docker compose down -v` as a generic reset command on RNA Bee: it would remove all project volumes, including PostgreSQL and simulation state.
