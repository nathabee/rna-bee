# VPS Installation

This document describes how to deploy RNA Bee on a Linux VPS with Docker Compose, Apache, and Certbot.

## Public URLs

```text
https://rna.nathabee.de/
https://rna.nathabee.de/api/
```

Routing:

```text
Apache :443
├── /      -> 127.0.0.1:8110 -> WordPress
└── /api/  -> 127.0.0.1:8111 -> Django
```

PostgreSQL, MariaDB, Redis, and Celery are not exposed publicly.

## DNS

Create DNS records for the VPS.

Example:

```text
Type: A
Name: rna
Value: <VPS IPv4>
```

Optional IPv6:

```text
Type: AAAA
Name: rna
Value: <VPS IPv6>
```

## Clone

Log in with a Docker-capable user:

```bash
cd ~
git clone https://github.com/nathabee/rna-bee.git
cd rna-bee
```

Create the environment file:

```bash
cp .env.example .env
nano .env
```

Example host ports:

```env
WORDPRESS_HOST_PORT=8110
DJANGO_HOST_PORT=8111
```

## Build and start

Validate:

```bash
docker compose config
```

Build:

```bash
docker compose build
```

For a clean rebuild:

```bash
docker compose build --no-cache
```

Start:

```bash
docker compose up -d
docker compose ps
```

## Local tests

WordPress:

```bash
curl -I http://127.0.0.1:8110/
```

Django:

```bash
curl http://127.0.0.1:8111/api/health/
```

Expected response:

```json
{"status":"ok","service":"rna-bee-api"}
```

## Apache

Enable required modules:

```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
sudo a2enmod ssl
```

Create:

```bash
sudo nano /etc/apache2/sites-available/rna.nathabee.de.conf
```

Configuration:

```apache
<VirtualHost *:80>
    ServerName rna.nathabee.de

    ProxyPreserveHost On
    ProxyRequests Off

    ProxyPass        /api/ http://127.0.0.1:8111/api/
    ProxyPassReverse /api/ http://127.0.0.1:8111/api/

    ProxyPass        / http://127.0.0.1:8110/
    ProxyPassReverse / http://127.0.0.1:8110/

    ErrorLog ${APACHE_LOG_DIR}/rna-bee-error.log
    CustomLog ${APACHE_LOG_DIR}/rna-bee-access.log combined
</VirtualHost>
```

Enable and reload:

```bash
sudo a2ensite rna.nathabee.de.conf
sudo apachectl configtest
sudo systemctl reload apache2
```

## HTTPS

Request and install the certificate:

```bash
sudo certbot --apache -d rna.nathabee.de
```

Certbot creates the HTTPS Apache configuration automatically, typically:

```text
/etc/apache2/sites-available/rna.nathabee.de-le-ssl.conf
```

Verify:

```bash
curl https://rna.nathabee.de/api/health/
curl -I https://rna.nathabee.de/
```

## Update deployment

```bash
cd ~/rna-bee
git pull
docker compose build
docker compose up -d

# omnipotent
docker compose run --rm wp-cli /bootstrap/bootstrap.sh
docker compose ps
```

If no image rebuild is required:

```bash
docker compose up -d
# WordPress-Bootstrap stehen:

docker compose run --rm wp-cli /bootstrap/bootstrap.sh

```

## Logs

```bash
docker compose logs --tail=100
```

or:

```bash
docker compose logs -f
```

## Stop

```bash
docker compose down
```

Do not use:

```bash
docker compose down -v
```

unless persistent Docker volumes should also be deleted.
