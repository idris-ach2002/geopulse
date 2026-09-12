# GeoPulse

GeoPulse est une plateforme géospatiale temps réel de découverte de ressources urbaines.

## V0

V0 initialise le monorepo, l'architecture et la chaîne de qualité.

Aucune entité métier GeoPulse n'est implémentée en V0.

## Prérequis

- Python 3.14
- Node.js 24
- npm
- Docker avec Docker Compose
- Git

## Backend Linux/macOS

    cd backend
    python3.14 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    pip install -e ".[dev]"
    uvicorn geopulse.api.fastapi.app:app --reload

## Backend Windows PowerShell

    cd backend
    py -3.14 -m venv .venv
    .venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    pip install -e ".[dev]"
    uvicorn geopulse.api.fastapi.app:app --reload

## Liveness

    GET http://127.0.0.1:8000/health/live

Réponse attendue :

    {"status":"ok"}

## Frontend

    cd frontend
    npm ci
    npm start -- --proxy-config proxy.conf.json

## Quality gate locale

    make ci

## Infrastructure V0

    docker compose -f infra/compose.yaml config

PostgreSQL/PostGIS, Redis, Kafka/Redpanda et Polars ne sont pas activés en V0.
