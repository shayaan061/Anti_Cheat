from fastapi import WebSocket, WebSocketDisconnect
import time

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

            # =========================
            # Calibration Phase
            # =========================

            if not session.is_calibrated:

                session.calibration_pitch_samples.append(
                    pose_result["pitch"]
                )

                session.calibration_yaw_samples.append(
                    pose_result["yaw"]
                )

                print(
                    f"Calibrating: "
                    f"{len(session.calibration_pitch_samples)}/100"
                )

                if (
                    len(
                        session.calibration_pitch_samples
                    ) >= 100
                ):

                    session.baseline_pitch = (
                        sum(
                            session.calibration_pitch_samples
                        )
                        /
                        len(
                            session.calibration_pitch_samples
                        )
                    )

                    session.baseline_yaw = (
                        sum(
                            session.calibration_yaw_samples
                        )
                        /
                        len(
                            session.calibration_yaw_samples
                        )
                    )

                    session.is_calibrated = True

                    print(
                        "\nCalibration Complete"
                    )

                    print(
                        f"Baseline Pitch: "
                        f"{session.baseline_pitch:.2f}"
                    )

                    print(
                        f"Baseline Yaw: "
                        f"{session.baseline_yaw:.2f}"
                    )

                continue

            # =========================
            # Normal Processing
            # =========================

            adjusted_pitch = (
                pose_result["pitch"]
                - session.baseline_pitch
            )

            adjusted_yaw = (
                pose_result["yaw"]
                - session.baseline_yaw
            )

            direction = direction_classifier.classify(
                adjusted_pitch,
                adjusted_yaw
            )

            session.pose_history.append(
                {
                    "timestamp": time.time(),

                    "pitch": adjusted_pitch,
                    "yaw": adjusted_yaw,
                    "roll": pose_result["roll"],

                    "direction": direction
                }
            )

            print(
                "History Size:",
                len(session.pose_history.get_all())
            )

            print(
                f"\nSession: {session.session_id}"
            )

            print(
                f"Adjusted Pitch: "
                f"{adjusted_pitch:.2f}"
            )

            print(
                f"Adjusted Yaw: "
                f"{adjusted_yaw:.2f}"
            )

            print(
                f"Roll: "
                f"{pose_result['roll']:.2f}"
            )

            print(
                f"Direction: {direction}"
            )

            await websocket.send_json(
                {
                    "type": "pose",

                    "sessionId": session_id,

                    "pitch": adjusted_pitch,
                    "yaw": adjusted_yaw,
                    "roll": pose_result["roll"],

                    "direction": direction,

                    "isCalibrated": session.is_calibrated,

                    "baselinePitch": session.baseline_pitch,
                    "baselineYaw": session.baseline_yaw
                }
            )

    except WebSocketDisconnect:

        print("Client disconnected")