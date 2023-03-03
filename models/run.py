from optuna_tuning.alg_samplers import SUPPORTED_ALGORITHMS
import bson
from typing import List
from bson import ObjectId
import motor.motor_asyncio as motor
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import JSONResponse

from models.pyObjectId import PyObjectId
from pydantic import BaseModel, Field
from pydantic.validators import datetime

"""
Application routes:
    POST / - creates a new trial.
    GET /env - view a list containing the best trials for each algorithm
    GET /env/alg - view a list containing the best trials for a single algorithm
    GET /{id} - view a single trial.
    DELETE /{id} - delete a trial.
"""

app = FastAPI()
client = motor.AsyncIOMotorClient("mongodb://localhost:27017")  # TODO does it find my config file?
db = client.runs  # or client["runs"]
collection = db.run  # or db["run"]


# A response body is the data your API sends to the client

# This is basically the superclass (contains the fields used by all subclasses)
class BaseRun(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    alg: str
    env: str
    co2: float  # todo necessary or just use Watts?
    trial: bson.binary.BINARY_SUBTYPE  # todo correct? The hyperparameters are in here
    tot_energy: float  # kWh
    tot_time: datetime  # end_time-start_time #todo result trial actually contains both!
    reward: float

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "LunarLander-v2_ppo",
                "trial": "object",
                "co2": 0.967,
                "tot_energy": 0.003749,
                "tot_time": "749.874",
                "reward": 4.79
            }
        }



# todo if this run is the best run up until now and there is a similarly good run in the db,
#  i should not post this run if the hyperparameteres of both runs are the same...
@app.post("/", response_description="Add new run", response_model=BaseRun)
async def create_run(run: BaseRun = Body(...)):
    # Decode JSON request body into Python dictionary before passing to client
    run = jsonable_encoder(run)
    new_run = await db[collection].insert_one(run)
    created_run = await db[collection].find_one({"_id": new_run.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_run)


@app.get("/env", response_description="List the top trial for each algorithm for selected env",
         response_model=List[BaseRun])
async def list_runs_for_env(env: str):
    runs = []

    # List of all supported algorithms
    algs = SUPPORTED_ALGORITHMS

    # A for loop that queries for each alg
    for index in range(len(algs)):
        # todo add check for if exists here
        cursor = await collection.find({'env': env, 'alg': algs[index]}).sort("reward", -1).limit(1)
        # Add the found trial to a list to be returned
        runs[index] = cursor

    return runs


@app.get("/env/alg", response_description="List the top trials for selected algorithm x env combo",
         response_model=List[BaseRun])
async def list_runs_for_env_alg(env: str, alg: str, limit: int):
    runs = await collection.find({'env': env, 'alg': alg}).sort("reward", -1).limit(limit).tolist()

    return runs


@app.get(
    "/{id}", response_description="Get a single run", response_model=BaseRun)
async def show_run(id: str):
    if (run := await collection.find_one({"_id": id})) is not None:
        return run

    raise HTTPException(status_code=404, detail=f"Run with id {id} not found")


@app.delete("/{id}", response_description="Delete a run")
async def delete_student(id: str):
    delete_result = await collection.delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Run with {id} not found")
