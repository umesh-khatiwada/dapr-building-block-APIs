# Simple FastAPI Dapr Example

A simple FastAPI application demonstrating Dapr building blocks including state management, pub/sub messaging, and service invocation.

## Features

- **State Management**: Save and retrieve state using Dapr state management building block
- **Pub/Sub**: Publish and subscribe to messages using Dapr pub/sub
- **Service Invocation**: Invoke other services through Dapr
- **Docker Compose**: Ready-to-run setup with Redis and Dapr sidecar

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Dapr CLI (optional, for local development)

## Quick Start with Docker Compose

```bash
# Build and run the application
docker-compose up --build

# The FastAPI app will be available at http://localhost:8000
# Dapr API will be available at http://localhost:3500
```

## Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run with Dapr sidecar:
```bash
dapr run --app-id fastapi-service --app-port 8000 --dapr-http-port 3500 -- python main.py
```

## API Endpoints

### Health Check
- **GET** `/health` - Check service health

### State Management
- **POST** `/state` - Save state
  ```json
  {
    "key": "user-123",
    "value": {"name": "John", "age": 30}
  }
  ```

- **GET** `/state/{key}` - Retrieve state by key

### Pub/Sub
- **POST** `/publish` - Publish a message
  ```json
  {
    "content": "New order placed",
    "pubsub_name": "pubsub",
    "topic": "orders"
  }
  ```

- **POST** `/subscribe/{topic}` - Dapr calls this when a message is published

### Service Invocation
- **POST** `/invoke` - Invoke another service
  ```json
  {
    "method": "other-service",
    "data": {"key": "value"}
  }
  ```

## Project Structure

```
.
├── main.py                          # FastAPI application
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Docker image configuration
├── docker-compose.yaml              # Docker Compose setup
├── dapr-components/                 # Dapr component configurations
│   ├── statestore.yaml             # State management component
│   └── pubsub.yaml                 # Pub/Sub component
├── .gitignore                       # Git ignore rules
└── README.md                        # This file
```

## Testing

View API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Example requests:

```bash
# Save state
curl -X POST http://localhost:8000/state \
  -H "Content-Type: application/json" \
  -d '{"key":"user-1","value":{"name":"Alice"}}'

# Get state
curl http://localhost:8000/state/user-1

# Publish message
curl -X POST http://localhost:8000/publish \
  -H "Content-Type: application/json" \
  -d '{"content":"Hello World","topic":"orders"}'

# Health check
curl http://localhost:8000/health
```

## Dapr Components

The project uses Redis for both state management and pub/sub messaging:

- **State Store** (`statestore.yaml`): Redis-backed persistent state
- **Pub/Sub** (`pubsub.yaml`): Redis-backed message broker

## Stopping the Application

```bash
docker-compose down

# Or with Dapr CLI
dapr stop
```

## Next Steps

- Explore [Dapr documentation](https://docs.dapr.io/)
- Add more building blocks (secrets, bindings, etc.)
- Integrate with additional services
- Deploy to Kubernetes

## References

- [Dapr Official Documentation](https://docs.dapr.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Python Dapr SDK](https://github.com/dapr/python-sdk)
