from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_and_unregister_participant():
    # Arrange
    activity_name = "Basketball Club"
    email = "student@example.edu"

    # Ensure a clean state
    activity = client.get("/activities").json()[activity_name]
    if email in activity["participants"]:
        client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Act: sign up
    signup_response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert: participant is added
    assert signup_response.status_code == 200
    assert email in client.get("/activities").json()[activity_name]["participants"]

    # Act: unregister
    unregister_response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    # Assert: participant is removed
    assert unregister_response.status_code == 200
    assert email not in client.get("/activities").json()[activity_name]["participants"]


def test_unregister_missing_participant_returns_404():
    activity_name = "Track and Field"
    email = "missing@example.edu"

    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"
