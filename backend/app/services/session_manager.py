from dataclasses import dataclass, field
from typing import Dict, List

from app.utils.ring_buffer import RingBuffer


@dataclass
class SessionState:
    session_id: str

    downward_duration: float = 0.0
    side_view_duration: float = 0.0

    suspicion_score: int = 0

    events: List = field(default_factory=list)

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