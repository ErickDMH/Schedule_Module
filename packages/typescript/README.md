# Schedule Module

A reusable, production-grade scheduling capability module designed for both human developers and AI agents.
It provides a robust scheduling system that allows projects to create, manage, and query events, routines, and time-based records across systems using a strictly structured PostgreSQL database.

## Architecture & Principles

- **Installability**: Can be initialized easily via `make initial`.
- **Backward Compatibility**: Migrations are versioned and immutable.
- **Agent-First Design**: Includes MCP integration and YAML action definitions for native AI consumption.
- **Human Usability**: Clean API, strongly typed Pydantic models.

## Usage

### 1. Installation

To initialize the database locally via Docker Compose, simply run:
```bash
make initial
```

This will:
1. Spin up a PostgreSQL container using `docker-compose.yml`.
2. Apply the initial schema and tables (`/db/ddl`).
3. Run all pending migrations (`/db/migrations`).

### 2. Python API

Use the `Schedule` service to interact with your data:

```python
from datetime import datetime, timezone
import asyncio
from uuid import uuid4
from src import Schedule, ScheduledRoutineCreate, RecurrencyType

async def main():
    async with Schedule() as schedule_service:
        routine = ScheduledRoutineCreate(
            name="Daily Standup",
            start_date_time=datetime.now(timezone.utc),
            end_date_time=datetime.now(timezone.utc),
            recurrency=RecurrencyType.daily
        )
        created_routine = await schedule_service.add_schedule(routine)
        print("Created Routine ID:", created_routine.id)

if __name__ == "__main__":
    asyncio.run(main())
```

### 3. Agent Integration

Refer to `agent/mcp.yaml` and `agent/actions.yaml` for using this module as a tool in AI workflows via MCP (Model Context Protocol).

## Infrastructure

We include boilerplate configurations for deployments:
- `infra/docker-compose.yml`: For local deployments
- `infra/terraform`: Example Terraform modules for AWS RDS Postgres deployments

## Publishing

The module includes a `.github/workflows/publish.yml` that automatically publishes to npm and PyPI whenever changes are merged into the `main` branch.
