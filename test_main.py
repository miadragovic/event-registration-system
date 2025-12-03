from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

TEST_EMAIL = "test@example.com"
TEST_PASSWORD = "test1234"   # MUST BE < 72 chars because bcrypt


def get_auth_headers():
    # Register test user
    client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD,
        },
    )

    # --- Make user admin for tests ---
    from database import SessionLocal
    from models import User

    db = SessionLocal()
    user = db.query(User).filter(User.email == TEST_EMAIL).first()
    if user:
        user.role = "admin"
        db.commit()
    db.close()
    # ---------------------------------

    # Login user
    login_res = client.post(
        "/auth/login",
        data={
            "username": TEST_EMAIL,
            "password": TEST_PASSWORD,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    token = login_res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_event():
    headers = get_auth_headers()

    response = client.post(
        "/events/",
        json={
            "name": "Test Event",
            "description": "Test Desc",
            "date": "2025-12-01T09:00:00Z",
            "location": "Online",
        },
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Test Event"


def test_create_registration():
    headers = get_auth_headers()

    # Create event
    event = client.post(
        "/events/",
        json={
            "name": "Reg Test Event",
            "description": "Test Desc",
            "date": "2025-12-05T09:00:00Z",
            "location": "Online",
        },
        headers=headers,
    ).json()

    event_id = event["id"]

    reg_response = client.post(
        "/registrations/",
        json={
            "event_id": event_id,
            "participant_name": "Tester",
            "participant_email": "test@example.com",
            "notes": "hello"
        },
        headers=headers,
    )

    print("REG RESPONSE:", reg_response.json())  # DEBUG PRINT

    assert reg_response.status_code == 200, \
        f"Unexpected status code: {reg_response.status_code}, body={reg_response.text}"

    data = reg_response.json()

    assert "event_id" in data, \
        f"event_id missing from response. Full response: {data}"

    assert data["event_id"] == event_id


def test_event_not_found():
    headers = get_auth_headers()

    reg_response = client.post(
        "/registrations/",
        json={
            "event_id": 999999,
            "participant_name": "Error Case",
            "participant_email": "error@example.com",
            "notes": "Invalid event",
        },
        headers=headers,
    )

    assert reg_response.status_code in (400, 404)
