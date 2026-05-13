.PHONY: help setup install build up down logs clean test docs run-local

help:
	@echo "LLM Call Dapr Example - Available commands:"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup          Create virtual environment and install dependencies"
	@echo "  make install        Install dependencies"
	@echo ""
	@echo "Running the Application:"
	@echo "  make build          Build Docker image"
	@echo "  make up             Start application with Docker Compose"
	@echo "  make down           Stop Docker Compose services"
	@echo "  make run-local      Run locally with Dapr CLI"
	@echo ""
	@echo "Development:"
	@echo "  make logs           View Docker Compose logs"
	@echo "  make clean          Clean up virtual environment and cache"
	@echo "  make test           Run example client"
	@echo ""
	@echo "Documentation:"
	@echo "  make docs           Show API documentation URL"

setup:
	bash setup.sh

install:
	pip install -r requirements.txt

build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	rm -rf venv __pycache__ .pytest_cache .coverage
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

run-local:
	@echo "Starting FastAPI app with Dapr sidecar..."
	dapr run --app-id llm-call-dapr --app-port 8000 --dapr-http-port 3500 --components-path ./dapr-components -- python main.py

test:
	@echo "Running example client..."
	python example_client.py

docs:
	@echo "API Documentation available at:"
	@echo "  Swagger UI: http://localhost:8000/docs"
	@echo "  ReDoc: http://localhost:8000/redoc"
	@echo ""
	@echo "Dapr API: http://localhost:3500"
