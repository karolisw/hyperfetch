from fastapi.testclient import TestClient
from main import app

# create a TestClient instance
client = TestClient(app)


def test_fetch_envs():
    response = client.get("/api/")
    assert response.status_code == 200
    assert response.json() == {"envs": []}  # replace with expected output


def test_create_run():
    run_data = {"name": "test run", "description": "test description"}
    response = client.post("/api/create", json=run_data)
    assert response.status_code == 201
    assert response.json()["name"] == "test run"
    assert response.json()["description"] == "test description"


def test_fetch_runs_for_env():
    response = client.get("/api/env_top_trials?env=my_env")
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_fetch_runs_for_env_alg():
    response = client.get("/api/alg_top_trials", params={"env": "my_env", "alg": "my_alg", "limit": 10})
    assert response.status_code == 200
    assert response.json() == {...}  # replace {...} with the expected JSON response


def test_fetch_run():
    # make a GET request to the endpoint with a valid run ID
    response = client.get("/api/runs/valid_run_id")

    # assert that the response has a status code of 200 (OK)
    assert response.status_code == 200

    # assert that the response contains the expected data
    expected_data = {"id": "valid_run_id", "name": "Run Name", "status": "completed"}
    assert response.json() == expected_data
