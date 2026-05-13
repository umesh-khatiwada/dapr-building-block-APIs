#!/usr/bin/env python3
"""Example client for the Dapr LLM conversation sample."""

import json
from typing import Any

import requests

BASE_URL = "http://localhost:8000"


def print_response(response: requests.Response, title: str = "Response") -> None:
    print(f"\n{title}:")
    print(f"Status: {response.status_code}")
    try:
        print(f"Data: {json.dumps(response.json(), indent=2)}")
    except Exception:
        print(f"Data: {response.text}")
    print("-" * 50)


def ask_llm(prompt: str, system_prompt: str | None = None) -> None:
    payload: dict[str, Any] = {"prompt": prompt}
    if system_prompt:
        payload["system_prompt"] = system_prompt

    response = requests.post(f"{BASE_URL}/chat", json=payload, timeout=30)
    print_response(response, "Chat Response")


def main() -> None:
    print("\nDapr LLM Call Example Client\n")
    try:
        ask_llm(
            "Write a one-sentence explanation of why openmetadata is useful for application developers.",
            "You are a helpful assistant that writes short, direct answers.",
        )
    except requests.exceptions.ConnectionError:
        print("\nCould not connect to the service.")
        print("Make sure the sample is running at http://localhost:8000")
        print("\nRun with Docker Compose:")
        print("  docker-compose up")
        print("\nOr with Dapr CLI:")
        print("  dapr run --app-id llm-call-dapr --app-port 8000 --components-path ./dapr-components -- python main.py")
    except Exception as exc:
        print(f"\nError: {exc}")


if __name__ == "__main__":
    main()
