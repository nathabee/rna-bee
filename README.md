# RNA Bee

Containerized playground for computational RNA folding and evolution experiments.

## Public routing

The project assumes:

- `https://rna.nathabee.de/` -> WordPress
- `https://rna.nathabee.de/api/` -> Django REST API

Apache runs on the VPS host and is intentionally **not** part of this Docker Compose project.

The Docker stack exposes only:

- WordPress -> `127.0.0.1:8080`
- Django -> `127.0.0.1:8000`

PostgreSQL, MariaDB, Redis and Celery have no public host ports.

## First deployment

As your Docker-capable VPS user:

```bash
unzip rna-bee-vps-skeleton.zip
cd rna-bee
cp .env.example .env
nano .env
docker compose config
docker compose build
docker compose up -d
docker compose ps
```

Local host tests:

```bash
curl http://127.0.0.1:8000/api/health/
curl -I http://127.0.0.1:8080/
```

Expected Django response:

```json
{"status":"ok","service":"rna-bee-api"}
```

Apache configuration requires a sudo-capable VPS user and is deliberately supplied only as an example under `apache/`.

## Architecture

WordPress is the presentation layer.

Django owns the REST API and experiment metadata.

Celery executes simulations asynchronously.

Redis is the Celery broker/cache.

PostgreSQL stores scientific/application data.

MariaDB is dedicated to WordPress.

The Celery worker image is where ViennaRNA and RNAstructure will be installed later.

## Current skeleton

The initial skeleton deliberately contains a working infrastructure and a placeholder folding-engine interface. It does **not** yet install ViennaRNA or RNAstructure. That will be the next development step, after the Docker stack is proven healthy on the VPS.


## License

![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
