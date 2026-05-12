from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from dapr.clients import DaprClient
import json

app = FastAPI(title="Dapr FastAPI Example", version="1.0.0")

# Models
class StateData(BaseModel):
    key: str
    value: dict

class Message(BaseModel):
    content: str
    pubsub_name: str = "pubsub"
    topic: str = "orders"

class InvokeRequest(BaseModel):
    method: str
    data: dict = None

# Initialize Dapr client
dapr_client = DaprClient()

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "dapr-fastapi-example"}

# State Management: Save state
@app.post("/state")
async def save_state(state_data: StateData):
    """Save state using Dapr state management"""
    try:
        dapr_client.save_state(
            store_name="statestore",
            key=state_data.key,
            value=json.dumps(state_data.value)
        )
        return {"message": f"State saved for key: {state_data.key}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# State Management: Get state
@app.get("/state/{key}")
async def get_state(key: str):
    """Retrieve state using Dapr state management"""
    try:
        response = dapr_client.get_state(
            store_name="statestore",
            key=key
        )
        if response.data:
            return {"key": key, "value": json.loads(response.data)}
        return {"key": key, "value": None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Pub/Sub: Publish message
@app.post("/publish")
async def publish_message(message: Message):
    """Publish a message using Dapr pub/sub"""
    try:
        dapr_client.publish_event(
            pubsub_name=message.pubsub_name,
            topic_name=message.topic,
            data=message.content
        )
        return {"message": f"Published to {message.topic}", "content": message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Pub/Sub: Subscribe endpoint (for Dapr to call)
@app.post("/subscribe/{topic}")
async def subscribe_handler(topic: str, body: dict):
    """Endpoint for Dapr to call when publishing to subscribed topics"""
    print(f"Received message from topic {topic}: {body}")
    return {"status": "processed"}

# Service Invocation: Invoke another service
@app.post("/invoke")
async def invoke_service(request: InvokeRequest):
    """Invoke another Dapr service"""
    try:
        response = dapr_client.invoke_method(
            app_id=request.method,
            method_name="invoke",
            data=request.data
        )
        return {"result": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Service Invocation: Example endpoint for other services to call
@app.post("/invoke")
async def invoke_handler(data: dict = None):
    """Endpoint for other services to invoke"""
    return {"message": "Invoked successfully", "received_data": data}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
