from app.services.direction_classifier import (
    DirectionClassifier
)

classifier = DirectionClassifier()

tests = [
    (0, 0),
    (20, 0),
    (-20, 0),
    (0, 20),
    (0, -20),
    (-20, 20),
    (-20, -20)
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