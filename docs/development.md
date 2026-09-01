# Development

This document describes the development workflow for RNA Bee.

Installation from a clean Git clone is documented in `install.md`. VPS-specific Apache and HTTPS configuration belongs in `install-vps.md`.

## Development model

The intended workflow is:

```text
local development
      |
      v
git commit
      |
      v
git push
      |
      v
GitHub
      |
      v
VPS git pull
      |
      v
Docker
```

The VPS checkout is a deployment target, not the primary development workspace.

Avoid editing tracked files directly on the VPS except when deliberately diagnosing or extracting an existing configuration. If a VPS-only correction is required, commit it immediately or reproduce it locally and return the VPS checkout to a clean state.

Check the working tree with:

```bash
git status
```

A deployment checkout should normally report:

```text
nothing to commit, working tree clean
```

## Repository ownership

RNA Bee keeps application code and reproducible configuration in Git.

```text
backend/
    Django application and scientific backend

wordpress/themes/rna-bee/
    RNA Bee Twenty Twenty-Five child theme

wordpress/plugins/rna-bee/
    RNA Bee WordPress functionality

wordpress/bootstrap/
    reproducible WordPress initialization

compose.yaml
    application services and networks

.env.example
    documented environment-variable template
```

Runtime state does not belong in Git.

Examples:

- MariaDB data
- PostgreSQL data
- WordPress uploads
- Redis persistence
- generated simulation results
- local `.env`

## WordPress child theme development

RNA Bee uses a child theme of Twenty Twenty-Five.

The child theme owns presentation concerns such as:

- `theme.json`
- color palette
- style variations such as `styles/dark.json`
- header and footer template parts
- page templates
- the `page-no-title` template
- reusable theme patterns
- theme-specific presentation code

Current files are stored below:

```text
wordpress/themes/rna-bee/
```

### Site Editor changes and the database

WordPress Site Editor changes are normally stored in the WordPress database first.

That means a visual change made through `wp-admin` is not automatically a Git change.

For reusable theme changes, the development flow is:

```text
WordPress Site Editor
        |
        v
database customization
        |
        v
Create Block Theme
        |
        v
theme files
        |
        v
Git
```

The WordPress `Create Block Theme` plugin can be used during theme development to export or save Site Editor customizations back into the child theme.

This is how the original RNA Bee child theme was extracted from the running WordPress installation.

### What should be edited in the Site Editor

The Site Editor is appropriate for visual block-theme structures such as:

- global styles
- palettes
- templates
- template parts
- header layout
- footer layout
- patterns

After the result is accepted, save/export it into the child theme and inspect the Git diff.

### What should be edited directly in code

Direct code editing is appropriate for files that are already part of the child theme or are not managed by the Site Editor.

Examples:

```text
wordpress/themes/rna-bee/theme.json
wordpress/themes/rna-bee/styles/dark.json
wordpress/themes/rna-bee/parts/header.html
wordpress/themes/rna-bee/parts/footer.html
wordpress/themes/rna-bee/templates/page-no-title.html
```

Always inspect the result:

```bash
git diff
```

before committing.

### Do not edit the parent theme

Do not modify Twenty Twenty-Five itself.

The parent theme is an external WordPress dependency and is installed by WordPress/WP-CLI.

All RNA Bee-specific presentation changes belong in:

```text
wordpress/themes/rna-bee/
```

## WordPress plugin development

Application behavior belongs in the RNA Bee plugin rather than in the child theme.

Current location:

```text
wordpress/plugins/rna-bee/
```

The plugin currently provides the frontend skeleton and the `[rna_bee]` shortcode.

The separation rule is:

```text
presentation / layout
    -> child theme

application behavior / API integration
    -> plugin
```

Future plugin responsibilities can include:

- RNA sequence input
- Django REST API calls
- experiment submission
- experiment status
- result rendering
- Gutenberg blocks
- RNA visualization integration

The plugin is bind-mounted into WordPress by Compose, so changes to files in the Git checkout are immediately visible inside the container.

## WordPress bootstrap development

The bootstrap script is:

```text
wordpress/bootstrap/bootstrap.sh
```

It is mounted read-only into the `wp-cli` tool container.

Run it with:

```bash
docker compose run --rm wp-cli /bootstrap/bootstrap.sh
```

The script must remain idempotent.

A second run must not create duplicate pages or otherwise corrupt an existing installation.

The bootstrap is responsible for reproducible application defaults, not for long-form project presentation content.

Good bootstrap content:

- site title
- theme activation
- plugin activation
- permalink configuration
- minimal application pages
- static front page
- template assignment

Content that does not belong in the bootstrap:

- portfolio articles
- architecture essays
- development history
- tutorials
- large demo databases

Project presentation belongs on `nathabee.de`; technical project documentation belongs under `docs/`.

## Updating WordPress theme or plugin code

Because the theme and plugin are bind-mounted, a Docker image rebuild is normally not required for PHP, HTML, JSON, or other files stored directly under the mounted directories.

After pulling changes on a running target:

```bash
git pull
```

verify that the files are visible inside WordPress:

```bash
docker compose exec wordpress \
  ls -la /var/www/html/wp-content/themes/rna-bee

docker compose exec wordpress \
  ls -la /var/www/html/wp-content/plugins/rna-bee
```

If the WordPress service definition or bind mounts changed, recreate that container:

```bash
docker compose up -d --force-recreate wordpress
```

This recreates the container but preserves the `wordpress_data` volume.

If bootstrap behavior changed:

```bash
docker compose run --rm wp-cli /bootstrap/bootstrap.sh
```

## Backend development

The Django service is built from:

```text
backend/Dockerfile
```

The Celery worker is built from:

```text
backend/Dockerfile.worker
```

After changing image contents or dependencies:

```bash
docker compose build
docker compose up -d
```

For a targeted rebuild:

```bash
docker compose build django celery-worker
docker compose up -d django celery-worker
```

Django starts by running:

```text
collectstatic
migrate
gunicorn
```

The Celery worker starts separately and communicates through Redis.

## Service boundaries

The current Compose architecture uses three networks:

```text
frontend
backend
wordpress_db
```

WordPress connects to:

```text
frontend
wordpress_db
```

Django connects to:

```text
frontend
backend
```

Celery, PostgreSQL, and Redis use the backend network.

MariaDB is isolated on the WordPress database network.

Only WordPress and Django publish host ports, both bound to `127.0.0.1`.

## Testing during development

Check container state:

```bash
docker compose ps
```

Test Django:

```bash
curl http://127.0.0.1:8111/api/health/
```

Test WordPress:

```bash
curl -I http://127.0.0.1:8110/
```

Check Django logs:

```bash
docker compose logs django --tail=100
```

Check Celery logs:

```bash
docker compose logs celery-worker --tail=100
```

Check WordPress logs:

```bash
docker compose logs wordpress --tail=100
```

The stabilization phase should additionally verify:

- WordPress frontend
- `/api/health/`
- DRF browsable API
- PostgreSQL connectivity
- Redis health
- Celery worker startup and broker connectivity

Those checks should be documented once the current infrastructure baseline is frozen.

## Deployment update workflow

After local changes are committed and pushed:

```bash
cd ~/rna-bee
git pull
```

If backend images changed:

```bash
docker compose build
docker compose up -d
```

If only bind-mounted WordPress theme/plugin files changed, no image build is required.

If Compose mounts for WordPress changed:

```bash
docker compose up -d --force-recreate wordpress
```

If WordPress bootstrap behavior changed:

```bash
docker compose run --rm wp-cli /bootstrap/bootstrap.sh
```

Finish by checking:

```bash
docker compose ps
git status
```

## Documentation responsibilities

Keep documentation split by purpose:

```text
README.md
    short project overview and links

docs/install.md
    normal installation from a Git clone

docs/install-vps.md
    VPS-specific Apache, reverse proxy, HTTPS, and host integration

docs/development.md
    development and Git/WordPress workflow

docs/
    architecture and other technical project documentation
```

Avoid duplicating long installation instructions in `README.md`. The README should link to the dedicated installation document.
