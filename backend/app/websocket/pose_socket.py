from fastapi import WebSocket, WebSocketDisconnect

from app.services.session_manager import SessionManager
from app.services.pose_estimator import PoseEstimator
from app.services.direction_classifier import DirectionClassifier

from app.models.request_models import LandmarkSet


session_manager = SessionManager()

pose_estimator = PoseEstimator()

direction_classifier = DirectionClassifier()


async def pose_websocket(websocket: WebSocket):

    await websocket.accept()

    print("Client connected")

    try:

        while True:

            data = await websocket.receive_json()

            session_id = data.get(
                "sessionId",
                "unknown"
            )

            frame_width = data.get(
                "frameWidth"
            )

            frame_height = data.get(
                "frameHeight"
            )

            landmarks = data.get(
                "landmarks"
            )

            if not landmarks:
                continue

            session = session_manager.create_session(
                session_id
            )

            landmark_set = LandmarkSet(
                **landmarks
            )

            pose_result = pose_estimator.estimate_pose(
                landmarks=landmark_set,
                frame_width=frame_width,
                frame_height=frame_height
            )

            direction = direction_classifier.classify(
                pose_result["pitch"],
                pose_result["yaw"]
            )

            print(
                f"\nSession: {session.session_id}"
            )

            print(
                f"Pitch: {pose_result['pitch']:.2f}"
            )

            print(
                f"Yaw: {pose_result['yaw']:.2f}"
            )

            print(
                f"Roll: {pose_result['roll']:.2f}"
            )

            print(
                f"Direction: {direction}"
            )

            await websocket.send_json(
                {
                    "type": "pose",

                    "sessionId": session_id,

                    "pitch": pose_result["pitch"],
                    "yaw": pose_result["yaw"],
                    "roll": pose_result["roll"],

                    "direction": direction
                }
            )

    except WebSocketDisconnect:

        print("Client disconnected")