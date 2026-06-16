from app.services.session_manager import SessionManager

manager = SessionManager()

session = manager.create_session("candidate123")

session.pose_history.append(
    {
        "pitch": -20,
        "yaw": 5
    }
)

print(session.pose_history.get_all())