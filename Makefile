.PHONY: backend-test backend-lint backend-format backend-typecheck frontend-test frontend-lint frontend-build test lint ci dev-backend dev-frontend

backend-test:
	cd backend && .venv/bin/python -m pytest -q --cov=geopulse --cov-branch --cov-report=term-missing --cov-fail-under=90

backend-lint:
	cd backend && .venv/bin/ruff check .

backend-format:
	cd backend && .venv/bin/ruff format --check .

backend-typecheck:
	cd backend && .venv/bin/mypy src/geopulse

frontend-test:
	cd frontend && npx ng test --watch=false

frontend-lint:
	cd frontend && npx ng lint

frontend-build:
	cd frontend && npm run build

test: backend-test frontend-test

lint: backend-lint backend-format backend-typecheck frontend-lint

ci: backend-lint backend-format backend-typecheck backend-test frontend-lint frontend-test frontend-build

dev-backend:
	cd backend && .venv/bin/uvicorn geopulse.api.fastapi.app:app --reload

dev-frontend:
	cd frontend && npm start -- --proxy-config proxy.conf.json
