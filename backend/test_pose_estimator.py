from app.services.pose_estimator import PoseEstimator

from app.models.request_models import (
    LandmarkPoint,
    LandmarkSet
)

landmarks = LandmarkSet(
    nose=LandmarkPoint(
        x=320,
        y=240
    ),

    chin=LandmarkPoint(
        x=320,
        y=380
    ),

    leftEye=LandmarkPoint(
        x=250,
        y=200
    ),

    rightEye=LandmarkPoint(
        x=390,
        y=200
    ),

    leftMouth=LandmarkPoint(
        x=280,
        y=300
    ),

    rightMouth=LandmarkPoint(
        x=360,
        y=300
    )
)

estimator = PoseEstimator()

result = estimator.estimate_pose(
    landmarks=landmarks,
    frame_width=1280,
    frame_height=720
)

print("Pitch:", result["pitch"])
print("Yaw:", result["yaw"])
print("Roll:", result["roll"])