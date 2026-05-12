#!/usr/bin/env python3
"""
Example client script to interact with the FastAPI Dapr application.
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"

def print_response(response: requests.Response, title: str = "Response"):
    """Pretty print API response"""
    print(f"\n{title}:")
    print(f"Status: {response.status_code}")
    try:
        print(f"Data: {json.dumps(response.json(), indent=2)}")
    except:
        print(f"Data: {response.text}")
    print("-" * 50)

def health_check():
    """Check service health"""
    print("=" * 50)
    print("HEALTH CHECK")
    print("=" * 50)
    response = requests.get(f"{BASE_URL}/health")
    print_response(response, "Health Check")

def save_state(key: str, value: Dict[str, Any]):
    """Save state to state store"""
    print("=" * 50)
    print("SAVE STATE")
    print("=" * 50)
    data = {
        "key": key,
        "value": value
    }
    print(f"Saving state: {json.dumps(data, indent=2)}")
    response = requests.post(f"{BASE_URL}/state", json=data)
    print_response(response, "Save State Response")

def get_state(key: str):
    """Retrieve state from state store"""
    print("=" * 50)
    print("GET STATE")
    print("=" * 50)
    print(f"Retrieving state for key: {key}")
    response = requests.get(f"{BASE_URL}/state/{key}")
    print_response(response, "Get State Response")

def publish_message(content: str, topic: str = "orders"):
    """Publish a message"""
    print("=" * 50)
    print("PUBLISH MESSAGE")
    print("=" * 50)
    data = {
        "content": content,
        "pubsub_name": "pubsub",
        "topic": topic
    }
    print(f"Publishing message: {json.dumps(data, indent=2)}")
    response = requests.post(f"{BASE_URL}/publish", json=data)
    print_response(response, "Publish Response")

def main():
    """Run example interactions"""
    print("\n🚀 FastAPI Dapr Example Client\n")
    
    try:
        # 1. Health check
        health_check()
        
        # 2. Save state
        save_state("user-123", {
            "name": "Alice",
            "email": "alice@example.com",
            "age": 30
        })
        
        # 3. Get state
        get_state("user-123")
        
        # 4. Publish message
        publish_message("New order: #12345", "orders")
        
        # 5. Publish another message
        publish_message("User registration complete", "users")
        
        print("\n✅ All examples completed successfully!\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the service.")
        print("Make sure the FastAPI service is running at http://localhost:8000")
        print("\nRun with Docker Compose:")
        print("  docker-compose up")
        print("\nOr with Dapr CLI:")
        print("  dapr run --app-id fastapi-service --app-port 8000 -- python main.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
