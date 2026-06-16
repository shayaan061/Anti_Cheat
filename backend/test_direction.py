from app.services.direction_classifier import (
    DirectionClassifier
)

classifier = DirectionClassifier()

tests = [
    (0, 10),
    (0, 20),
    (0, -20),
    (25, 0),
    (-25, 0),
    (-25, 20),
    (25, -20)
]

for pitch, yaw in tests:

    direction = classifier.classify(
        pitch,
        yaw
    )

    print(
        f"Pitch={pitch}, "
        f"Yaw={yaw} "
        f"-> {direction}"
    )
