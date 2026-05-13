import json
import os
from typing import Any

import requests
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

APP_PORT = int(os.getenv("APP_PORT", "8000"))
DAPR_HOST = os.getenv("DAPR_HOST", "localhost")
DAPR_HTTP_PORT = int(os.getenv("DAPR_HTTP_PORT", "3500"))
CONVERSATION_COMPONENT = os.getenv("CONVERSATION_COMPONENT", "llm-chat")
DEFAULT_SYSTEM_PROMPT = os.getenv(
    "DEFAULT_SYSTEM_PROMPT",
    "You are a concise assistant. Keep responses short and practical.",
)
USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"

app = FastAPI(title="Dapr LLM Call Example", version="1.0.0")


class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="User message to send to the conversation API")
    system_prompt: str | None = Field(
        default=None,
        description="Optional system prompt. If omitted, a default one is used.",
    )
    temperature: float = Field(default=0.2, ge=0.0, le=2.0)


class ChatResponse(BaseModel):
    component: str
    prompt: str
    system_prompt: str
    reply: str
    raw_response: dict[str, Any]


@app.get("/health")
async def health_check() -> dict[str, Any]:
    return {
        "status": "ok",
        "service": "llm-call-dapr",
        "component": CONVERSATION_COMPONENT,
        "dapr_http_port": DAPR_HTTP_PORT,
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    system_prompt = request.system_prompt or DEFAULT_SYSTEM_PROMPT
    
    # Use mock response if enabled
    if USE_MOCK:
        return _create_mock_response(request.prompt, system_prompt)
    
    url = f"http://{DAPR_HOST}:{DAPR_HTTP_PORT}/v1.0-alpha2/conversation/{CONVERSATION_COMPONENT}/converse"

    payload = {
        "inputs": [
            {
                "messages": [
                    {
                        "ofSystem": {
                            "name": "sample-system",
                            "content": [{"text": system_prompt}],
                        }
                    },
                    {
                        "ofUser": {
                            "name": "sample-user",
                            "content": [{"text": request.prompt}],
                        }
                    },
                ],
                "scrubPII": False,
            }
        ],
        "temperature": request.temperature,
    }

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"Dapr conversation call failed: {exc}") from exc

    try:
        data = response.json()
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=502, detail="Dapr returned a non-JSON response") from exc

    reply = _extract_reply(data)
    if reply is None:
        raise HTTPException(status_code=502, detail="Dapr response did not contain a conversation reply")

    return ChatResponse(
        component=CONVERSATION_COMPONENT,
        prompt=request.prompt,
        system_prompt=system_prompt,
        reply=reply,
        raw_response=data,
    )


def _extract_reply(payload: dict[str, Any]) -> str | None:
    outputs = payload.get("outputs")
    if not outputs:
        return None

    first_output = outputs[0]
    choices = first_output.get("choices") or []
    if not choices:
        return None

    message = choices[0].get("message") or {}
    reply = message.get("content")
    if isinstance(reply, str) and reply.strip():
        return reply

    return None


def _create_mock_response(prompt: str, system_prompt: str) -> ChatResponse:
    """Create a mock conversation response for testing without Dapr"""
    mock_reply = f"Mock response: I received your prompt '{prompt}' with system context: {system_prompt[:40]}..."
    
    mock_data = {
        "outputs": [
            {
                "choices": [
                    {
                        "message": {
                            "content": mock_reply
                        }
                    }
                ]
            }
        ]
    }
    
    return ChatResponse(
        component=f"{CONVERSATION_COMPONENT} (mock)",
        prompt=prompt,
        system_prompt=system_prompt,
        reply=mock_reply,
        raw_response=mock_data,
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=APP_PORT)
