from dataclasses import dataclass, field
from typing import Dict, List

from app.utils.ring_buffer import RingBuffer


@dataclass
class SessionState:
    session_id: str

    # Calibration
    baseline_pitch: float = 0.0
    baseline_yaw: float = 0.0

    is_calibrated: bool = False

    calibration_pitch_samples: List[float] = field(
        default_factory=list
    )

    calibration_yaw_samples: List[float] = field(
        default_factory=list
    )

    # Duration Tracking
    downward_duration: float = 0.0
    side_view_duration: float = 0.0

    # Scoring
    suspicion_score: int = 0

    # Events
    events: List = field(default_factory=list)

    # Pose History
    pose_history: RingBuffer = field(
        default_factory=lambda: RingBuffer(max_size=900)
    )


class SessionManager:

    def __init__(self):
        self.sessions: Dict[str, SessionState] = {}

    def create_session(self, session_id: str):

        if session_id not in self.sessions:
            self.sessions[session_id] = SessionState(
                session_id=session_id
            )

        return self.sessions[session_id]

    def get_session(self, session_id: str):

        return self.sessions.get(session_id)

    def remove_session(self, session_id: str):

        if session_id in self.sessions:
            del self.sessions[session_id]