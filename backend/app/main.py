from fastapi import FastAPI, WebSocket

from app.websocket.pose_socket import pose_websocket
from app.models.request_models import PoseFrame
from app.models.response_models import PoseResult

app = FastAPI(
    title="Interview Head Pose API",
    version="1.0.0"
)


@app.get("/")
async def root():
    return {
        "status": "running",
        "service": "head-pose-monitor"
    }


@app.websocket("/ws/pose")
async def websocket_endpoint(websocket: WebSocket):
    await pose_websocket(websocket)