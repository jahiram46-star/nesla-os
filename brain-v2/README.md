# NESLA Brain V2

Brain V2 is the central intelligence service for the NESLA ecosystem. This repository provides the initial production-oriented FastAPI architecture for the intelligence layer, with clean extension points for knowledge, memory, reasoning, decisioning, planning, task, project, execution, learning, and MRM integration capabilities.

Complex business logic is intentionally not implemented yet. The current focus is stable structure, configuration, dependency wiring, startup/bootstrap behavior, API routing, database connectivity, Redis connectivity, and module boundaries.

## Repository Structure

```text
brain-v2/
├── brain_v2/
│   ├── api/
│   │   ├── routes/
│   │   ├── deps.py
│   │   └── router.py
│   ├── core/
│   │   ├── bootstrap.py
│   │   ├── config.py
│   │   ├── container.py
│   │   ├── lifespan.py
│   │   └── logging.py
│   ├── db/
│   │   ├── base.py
│   │   ├── models.py
│   │   └── session.py
│   ├── modules/
│   │   ├── decision/
│   │   ├── execution/
│   │   ├── interfaces.py
│   │   ├── knowledge/
│   │   ├── learning/
│   │   ├── memory/
│   │   ├── mrm_connector/
│   │   ├── planning/
│   │   ├── project/
│   │   ├── reasoning/
│   │   └── task/
│   │   └── test_*.py
│   ├── schemas/
│   ├── services/
│   └── main.py
├── tests/
├── .dockerignore
├── .env.example
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Local Development

```bash
cd brain-v2
python3.14 -m venv .venv
. .venv/Scripts/activate
pip install -r requirements.txt
uvicorn brain_v2.main:create_app --factory --reload
```

API docs are available at:

- `http://localhost:8000/docs`
- `http://localhost:8000/redoc`

## Docker

```bash
cd brain-v2
docker compose up --build
```

## Health Checks

- `GET /health`
- `GET /api/v1/health`
- `GET /api/v1/modules`
- `GET /api/v1/{module}/status`

## Architecture Notes

- `core/config.py` centralizes environment-driven settings.
- `core/container.py` owns application-level dependency instances.
- `core/lifespan.py` wires startup and shutdown lifecycle behavior.
- `db/session.py` creates async SQLAlchemy engine and session factories.
- `api/deps.py` exposes FastAPI dependency providers.
- Each module owns its router, schemas, and service.

## Brain Modules

1. Knowledge Engine
2. Memory Engine
3. Reasoning Engine
4. Decision Engine
5. Planning Engine
6. Task Engine
7. Project Engine
8. Execution Engine
9. Learning Engine
10. MRM Connector
