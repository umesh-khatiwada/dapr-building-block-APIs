# Dapr LLM Call Example

A small FastAPI app that calls the Dapr Conversation API and is ready to run with a local `conversation.echo` component.

## What it demonstrates

- Calling Dapr's alpha2 conversation endpoint from a Python app
- Sending a system prompt and a user prompt through the sidecar
- Returning the assistant response as JSON
- Running without external LLM credentials by default

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- Dapr CLI for local development

## Quick Start with Docker Compose

```bash
docker-compose up --build
```

The app will be available at `http://localhost:8000`.

## Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run with Dapr sidecar:
```bash
dapr run --app-id llm-call-dapr --app-port 8000 --components-path ./dapr-components -- python main.py
```

## API Endpoints

### Health Check
- **GET** `/health` - Returns service and Dapr configuration details

### Chat
- **POST** `/chat` - Sends a prompt to Dapr Conversation and returns the generated reply

Example request:

```json
{
  "prompt": "Explain Dapr in one sentence.",
  "system_prompt": "You are a helpful assistant.",
  "temperature": 0.2
}
```

Example response:

```json
{
  "component": "llm-chat",
  "prompt": "Explain Dapr in one sentence.",
  "system_prompt": "You are a helpful assistant.",
  "reply": "...",
  "raw_response": {}
}
```

## Dapr Component

This sample ships with a local `conversation.echo` component named `llm-chat` so you can run it offline.

To use a real provider instead, replace the component in `dapr-components/` with one of the supported conversation components and keep the app code unchanged.

## Testing

Run the included client:

```bash
python example_client.py
```

## Stopping the Application

```bash
docker-compose down
```

## References

- [Dapr Official Documentation](https://docs.dapr.io/)
- [Conversation API](https://docs.dapr.io/developing-applications/building-blocks/llm-call/)
- [Python Dapr SDK](https://github.com/dapr/python-sdk)
