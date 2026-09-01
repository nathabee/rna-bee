# RNA Bee

RNA Bee is an open-source playground for computational RNA folding, mutation, and evolution experiments.

> [!WARNING]
> **RNA Bee is under active development.**
>
> The current release is an infrastructure and platform prototype. APIs, data models, WordPress integration, Docker configuration, and installation procedures may still change.
>
> Do not use this version for production workloads or scientific conclusions.

 
The project combines a WordPress-based interface with a Python/Django scientific backend and asynchronous simulation infrastructure.

The goal is to build a reproducible environment where RNA sequences can be generated, mutated, folded, compared, and eventually evolved under configurable selection criteria.

## Current platform

RNA Bee currently provides:

- WordPress frontend
- RNA Bee child theme based on Twenty Twenty-Five
- RNA Bee WordPress plugin skeleton
- reproducible WordPress bootstrap with WP-CLI
- Django REST Framework API
- PostgreSQL
- MariaDB
- Redis
- Celery
- Docker Compose
- Apache reverse-proxy deployment
- HTTPS with Certbot
- RNA sequence generator
- point mutation module
- RNA folding engine abstraction

Scientific folding engines such as ViennaRNA and RNAstructure are the next layer to be integrated into the simulation backend.

## Architecture

```text
Browser
   |
   v
Apache / HTTPS
   |
   +---- / ------> WordPress
   |                 |
   |                 v
   |              MariaDB
   |
   +---- /api/ --> Django REST API
                     |
              +------+------+
              |             |
              v             v
         PostgreSQL       Redis
                            |
                            v
                       Celery Worker
                            |
                            v
                    Simulation Engine
                            |
                            v
                     Folding Adapter
                       /         \
                      v           v
                ViennaRNA    RNAstructure
````

Only WordPress and Django are exposed through the host reverse proxy.

PostgreSQL, MariaDB, Redis, and Celery remain internal Docker services.

## WordPress

The WordPress layer is reproducible from Git.

The repository contains:

```text
wordpress/
├── themes/
│   └── rna-bee/
├── plugins/
│   └── rna-bee/
└── bootstrap/
    └── bootstrap.sh
```

A fresh installation automatically activates the RNA Bee child theme and plugin and creates the minimal application pages:

```text
Home
About RNA Bee
Explore
```

Long-form project presentation and development articles are intentionally kept outside the application itself.

## Documentation

### Installation

Install RNA Bee from a fresh Git clone:

[Installation guide](docs/install.md)

### VPS deployment

Apache reverse proxy, HTTPS, Certbot, and VPS-specific deployment:

[VPS installation guide](docs/install-vps.md)

### Development

WordPress child-theme workflow, plugin development, bootstrap changes, Docker rebuilds, and deployment workflow:

[Development guide](docs/development.md)

## Public instance

RNA Bee:

[https://rna.nathabee.de/](https://rna.nathabee.de/)

API health endpoint:

[https://rna.nathabee.de/api/health/](https://rna.nathabee.de/api/health/)

## Repository philosophy

The repository contains the application definition:

```text
Git
├── application code
├── Django backend
├── WordPress child theme
├── WordPress plugin
├── WordPress bootstrap
├── Docker configuration
└── technical documentation
```

Runtime state stays outside Git:

```text
Docker volumes
├── WordPress data
├── MariaDB
├── PostgreSQL
├── Redis
└── simulation results
```

The target is that the platform can be recreated from:

```text
Git repository
+
.env configuration
+
Docker
```

without depending on manual changes inside existing containers.

## Status

RNA Bee is currently in the infrastructure and platform-stabilization phase.

The next milestones are:

* verify all platform services
* integrate the first RNA folding engine
* implement persistent experiment models
* add mutation and fitness strategies
* run the first evolutionary simulation
* expose simulations through WordPress blocks

## License

![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)

RNA Bee is licensed under the Apache License 2.0.

See [LICENSE](LICENSE).

 