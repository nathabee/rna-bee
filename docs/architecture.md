# Architecture

```mermaid
flowchart TB
    U[Browser] --> A[Apache on VPS]

    A -->|rna.nathabee.de/| WP[WordPress]
    A -->|rna.nathabee.de/api/| DJ[Django REST API]

    WP --> MDB[(MariaDB)]
    WP --> DJ

    DJ --> PG[(PostgreSQL)]
    DJ --> R[(Redis)]

    R --> CW[Celery Worker]

    CW --> SIM[Simulation Engine]
    SIM --> FA[Folding Adapter]
    FA --> V[ViennaRNA - next stage]
    FA --> RS[RNAstructure - later]

    CW --> PG
    CW --> VOL[(Simulation Results Volume)]
```

## VPS boundary

Apache is shared infrastructure on the VPS and is not owned by this repository's Docker Compose stack.

The RNA Bee project only owns its Docker services and localhost-bound ports.
