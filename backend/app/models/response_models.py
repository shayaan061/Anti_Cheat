from pydantic import BaseModel


class PoseResult(BaseModel):
    pitch: float

    yaw: float

    roll: float

    headDirection: str

    downwardDuration: float

    sideViewDuration: float

    suspicionScore: int

    suspiciousEvents: list