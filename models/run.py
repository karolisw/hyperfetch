import uuid

from fastapi import FastAPI
from pydantic import BaseModel, Field
from pydantic.validators import datetime

app = FastAPI()

# A response body is the data your API sends to the client

# This is basically the superclass (contains the fields used by all subclasses)
class BaseRun(BaseModel):
    co2: float
    start_time: datetime  # send both start and end time in order to calculate tot_time
    end_time: datetime
    algorithm: str
    max_reward: float
    avg_reward: float


# Models the request body of the "Run"-entity (meaning sent by/from client to this API)
# Inherits from BaseRun instead of BaseModel
class RunIn(BaseRun):
    run_id: str = Field(default_factory=uuid.uuid4, alias="run_id")
    hyperparameter_dict: list[tuple]


# Posts into the db and returns the BaseRun
@app.post("/run/")
async def post_run(run: RunIn) -> BaseRun:
    return run
