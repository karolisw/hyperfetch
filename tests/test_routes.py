from fastapi.testclient import TestClient
from motor.motor_asyncio import AsyncIOMotorClient
from main import app
from src.db_config.auth_connection import MONGODB_URL
from src.db_config.mongodb import db

# create a TestClient instance
client = TestClient(app)

# To bypass middleware
headers = {
    "Origin": "https://www.hyperfetch.online",
    "Host": "hyperfetch-backend.azurewebsites.net"
}


# Connect to db
def connect():
    db.client = AsyncIOMotorClient(str(MONGODB_URL))


def test_fetch_envs():
    connect()
    response = client.get("/api/", headers=headers)
    assert response.status_code == 200
    assert response.json() == [{'env': 'Acrobot-v1'},
                               {'env': 'CartPole-v1'},
                               {'env': 'LunarLander-v2'},
                               {'env': 'MountainCar-v0'},
                               {'env': 'MountainCarContinuous-v0'},
                               {'env': 'Pendulum-v1'}]


id_found = ""


def test_fetch_runs_for_env():
    connect()
    # When selected env is Pendulum-v1
    response = client.get("/api/env_top_trials?env=Pendulum-v1", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_fetch_runs_for_env_alg():
    connect()
    response = client.get("/api/alg_top_trials", params={"env": "Pendulum-v1", "alg": "ppo", "limit": 10},
                          headers=headers
                          )
    assert response.status_code == 200
    assert len(response.json()) == 10


def test_fetch_run():
    connect()
    # make a GET request to the endpoint with a valid run ID
    response = client.get("/api/runs/5d85547a-9386-49f6-9e4b-aaed8375fb5e", headers=headers)

    # assert that the response has a status code of 200 (OK)
    assert response.status_code == 200

    # assert that the response contains the expected data
    assert response.json()["run_id"] == "5d85547a-9386-49f6-9e4b-aaed8375fb5e"
    assert response.json()["project_name"] == "MountainCarContinuous-v0_halving_cmaes"


# REMOVED ENDPOINTS
"""
def test_remove_run():
    connect()
    # Create a sample run ID for testing
    run_id = id_found

    # Make a DELETE request to the endpoint with the run ID
    response = client.delete(f"/api/delete/{run_id}")

    # Assert that the response status code is 204 (No Content)
    assert response.status_code == 204
    
def test_create_run():
    connect()
    run_data = {
        "trial": {"batch_size": 256,
                  "buffer_size": 50000,
                  "exploration_final_eps": 0.10717928118310233,
                  "exploration_fraction": 0.3318973226098944,
                  "gamma": 0.9,
                  "learning_rate": 0.0002126832542803243,
                  "learning_starts": 10000,
                  "net_arch": "medium",
                  "subsample_steps": 4,
                  "target_update_interval": 1000,
                  "train_freq": 8},
        "energy_consumed": 0.124,
        "cpu_model": "AMD Ryzen 5800H",
        "gpu_model": "NVIDIA geforce RTX 3070",
        "CO2_emissions": 0.032,
        "alg": "td3",
        "git_link": "github.com/user/some_project",
        "project_name": "some_project",
        "env": "LunarLander-v2",
        "total_time": "0:04:16.842800",
        "sampler": "tpe",
        "pruner": "median",
        "n_trials": "24",
        "country": "Norway",
        "region": "Trønderlag",
        "cloud_provider": "",
        "cloud_region": "",
        "os": "Windows 11",
        "python_version": "3.10.9",
        "reward": 22.5
    }

    # Make the payload valid by turning it into a Pydantic model
    serialized_payload = jsonable_encoder(RunCreate(**run_data))

    response = client.post("/api/create", json=serialized_payload, headers=headers)
    assert response.status_code == 201

    response_json = response.json()

    # Fetch the run id
    id_found = response_json["run_id"]
    assert id_found != 0


def extra_parameters_fails():
    connect()
    run_data = {
        "run_id": 1,
        "trial": {"batch_size": 256,
                  "buffer_size": 50000,
                  "exploration_final_eps": 0.10717928118310233,
                  "exploration_fraction": 0.3318973226098944,
                  "gamma": 0.9,
                  "learning_rate": 0.0002126832542803243,
                  "learning_starts": 10000,
                  "net_arch": "medium",
                  "subsample_steps": 4,
                  "target_update_interval": 1000,
                  "train_freq": 8},
        "energy_consumed": 0.124,
        "cpu_model": "AMD Ryzen 5800H",
        "gpu_model": "NVIDIA geforce RTX 3070",
        "CO2_emissions": 0.032,
        "alg": "td3",
        "git_link": "github.com/user/some_project",
        "project_name": "some_project",
        "env": "LunarLander-v2",
        "total_time": "0:04:16.842800",
        "sampler": "tpe",
        "pruner": "median",
        "n_trials": "24",
        "country": "Norway",
        "region": "Trønderlag",
        "cloud_provider": "",
        "cloud_region": "",
        "os": "Windows 11",
        "python_version": "3.10.9",
        "reward": 22.5
    }

    # Make the payload valid by turning it into a Pydantic model
    serialized_payload = jsonable_encoder(RunCreate(**run_data))

    response = client.post("/api/create", json=serialized_payload, headers=headers)
    assert response.is_error
"""
