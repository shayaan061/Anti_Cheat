class DirectionClassifier:

    def __init__(
        self,
        pitch_threshold: float = 5.0,
        yaw_threshold: float = 17.0
    ):
        self.pitch_threshold = pitch_threshold
        self.yaw_threshold = yaw_threshold

    def classify(
        self,
        pitch: float,
        yaw: float
    ) -> str:

        if (
            abs(pitch) < self.pitch_threshold
            and
            abs(yaw) < self.yaw_threshold
        ):
            return "CENTER"

        vertical = ""
        horizontal = ""

        if pitch <= -self.pitch_threshold:
            vertical = "DOWN"

        elif pitch >= self.pitch_threshold:
            vertical = "UP"

        if yaw <= -self.yaw_threshold:
            horizontal = "LEFT"

        elif yaw >= self.yaw_threshold:
            horizontal = "RIGHT"

        if vertical and horizontal:
            return f"{vertical}_{horizontal}"

        if vertical:
            return vertical

        if horizontal:
            return horizontal

        return "CENTER"