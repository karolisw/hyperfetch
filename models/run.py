import bson
from bson import ObjectId
import motor.motor_asyncio as motor
from fastapi import FastAPI

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
    CO2_emissions: float
    energy_consumed: float  # kWh
    cpu_model: str
    gpu_model: str
    trial: bson.binary.BINARY_SUBTYPE  # todo correct? The hyperparameters are in here
    total_time: datetime  # end_time-start_time #todo result trial actually contains both!
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

