from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_event():
    response = client.post("/events/", json={
        "name": "Test Event",
        "description": "Test Desc",
        "date": "2025-12-01T09:00:00Z",
        "location": "Online"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Test Event"

def test_list_events():
    response = client.get("/events/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_registration():
    # Get current events, use first event's id
    events_resp = client.get("/events/")
    events = events_resp.json()
    assert events, "No events available for registration test"
    event_id = events[0]["id"]

    reg_response = client.post("/registrations/", json={
        "event_id": event_id,
        "participant_name": "John Doe",
        "participant_email": "john@example.com",
        "notes": "Wants workshop materials"
    })
    assert reg_response.status_code == 200
    assert reg_response.json()["participant_name"] == "John Doe"

def test_list_registrations():
    response = client.get("/registrations/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_event_not_found():
    # Attempt to register with invalid event_id
    reg_response = client.post("/registrations/", json={
        "event_id": 999999,
        "participant_name": "Error Case",
        "participant_email": "error@example.com",
        "notes": "Invalid event"
    })
    assert reg_response.status_code in [400, 404]  # Depending on your error handling
