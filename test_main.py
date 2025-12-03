from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def get_auth_headers():
    client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "test123",
        "name": "Tester"
    })

    resp = client.post("/auth/login", data={
        "username": "test@example.com",
        "password": "test123"
    })

    assert resp.status_code == 200, f"Login failed: {resp.text}"

    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_create_event():
    headers = get_auth_headers()
    response = client.post("/events/", json={
        "name": "Test Event",
        "description": "Test Desc",
        "date": "2025-12-01T09:00:00Z",
        "location": "Online"
    }, headers=headers)

    assert response.status_code == 200
    assert response.json()["name"] == "Test Event"


def test_list_events():
    response = client.get("/events/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_registration():
    headers = get_auth_headers()

    events_resp = client.get("/events/")
    events = events_resp.json()
    assert events, "No events available for registration test"

    event_id = events[0]["id"]

    reg_response = client.post("/registrations/", json={
        "event_id": event_id,
        "participant_name": "John Doe",
        "participant_email": "john@example.com",
        "notes": "Wants workshop materials"
    }, headers=headers)

    assert reg_response.status_code == 200
    assert reg_response.json()["participant_name"] == "John Doe"


def test_list_registrations():
    response = client.get("/registrations/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_event_not_found():
    headers = get_auth_headers()

    reg_response = client.post("/registrations/", json={
        "event_id": 999999,
        "participant_name": "Error Case",
        "participant_email": "error@example.com",
        "notes": "Invalid event"
    }, headers=headers)

    assert reg_response.status_code in [400, 404]

