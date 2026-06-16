from pydantic import BaseModel


class LandmarkPoint(BaseModel):
    x: float
    y: float


class LandmarkSet(BaseModel):
    nose: LandmarkPoint
    chin: LandmarkPoint

    leftEye: LandmarkPoint
    rightEye: LandmarkPoint

    leftMouth: LandmarkPoint
    rightMouth: LandmarkPoint


class PoseFrame(BaseModel):
    type: str

    sessionId: str

    timestamp: int

    frameNumber: int

    frameWidth: int
    frameHeight: int

    landmarks: LandmarkSet