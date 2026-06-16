import cv2
import numpy as np
from scipy.spatial.transform import Rotation as R


class PoseEstimator:

    def __init__(self):

        self.model_points = np.array(
            [
                (0.0, 0.0, 0.0),          # Nose
                (0.0, -330.0, -65.0),     # Chin
                (-225.0, 170.0, -135.0),  # Left Eye
                (225.0, 170.0, -135.0),   # Right Eye
                (-150.0, -150.0, -125.0), # Left Mouth
                (150.0, -150.0, -125.0)   # Right Mouth
            ],
            dtype=np.float64
        )

    def estimate_pose(
        self,
        landmarks,
        frame_width,
        frame_height
    ):

        focal_length = frame_width

        center = (
            frame_width / 2,
            frame_height / 2
        )

        camera_matrix = np.array(
            [
                [focal_length, 0, center[0]],
                [0, focal_length, center[1]],
                [0, 0, 1]
            ],
            dtype=np.float64
        )

        dist_coeffs = np.zeros(
            (4, 1),
            dtype=np.float64
        )

        image_points = np.array(
            [
                [landmarks.nose.x, landmarks.nose.y],
                [landmarks.chin.x, landmarks.chin.y],
                [landmarks.leftEye.x, landmarks.leftEye.y],
                [landmarks.rightEye.x, landmarks.rightEye.y],
                [landmarks.leftMouth.x, landmarks.leftMouth.y],
                [landmarks.rightMouth.x, landmarks.rightMouth.y]
            ],
            dtype=np.float64
        )

        success, rotation_vector, translation_vector = cv2.solvePnP(
            self.model_points,
            image_points,
            camera_matrix,
            dist_coeffs,
            flags=cv2.SOLVEPNP_ITERATIVE
        )

        if not success:
            raise Exception("solvePnP failed")

        rotation_matrix, _ = cv2.Rodrigues(
            rotation_vector
        )

        rotation = R.from_matrix(
            rotation_matrix
        )

        pitch, yaw, roll = rotation.as_euler(
            "xyz",
            degrees=True
        )

        # Normalize pitch around 0
        if pitch > 90:
            pitch -= 180

        elif pitch < -90:
            pitch += 180

        # Fix inverted pitch axis
        pitch = -pitch

        return {
            "pitch": float(pitch),
            "yaw": float(yaw),
            "roll": float(roll),

            "rotation_vector": rotation_vector,
            "translation_vector": translation_vector
        }