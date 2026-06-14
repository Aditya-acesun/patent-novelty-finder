.PHONY: up down logs build restart clean setup

## Start all services
up:
	docker compose up -d

## Start all services with live logs
up-logs:
	docker compose up

## Stop all services
down:
	docker compose down

## Stop and remove all volumes (DELETES ALL DATA)
clean:
	docker compose down -v --remove-orphans

## Rebuild all images
build:
	docker compose build --no-cache

## View logs (all services or pass s=backend)
logs:
	docker compose logs -f $(s)

## Restart a single service: make restart s=backend
restart:
	docker compose restart $(s)

## First-time setup: copy env and pull images
setup:
	@cp -n .env.example .env || true
	@echo "✅ .env created — fill in your secrets before running 'make up'"
	docker compose pull qdrant redis

## Open Swagger UI
swagger:
	open http://localhost:4000/api/docs

## Open Qdrant dashboard
qdrant-ui:
	open http://localhost:6333/dashboard

## Tail celery worker logs
celery-logs:
	docker compose logs -f celery-worker
