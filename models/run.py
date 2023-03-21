from bson import ObjectId

from models.pyObjectId import PyObjectId
from pydantic import Field
from typing import Dict, Union, List
import RWModel


class BaseRun(RWModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    trial: Dict[str, Union[str, float]]
    name: str
    energy_comsumed: float
    cpu_model: str
    gpu_model: str
    CO2_emissions: float
    alg: str
    env: str
    total_time: str  # end_time-start_time
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


class RunInResponse(RWModel):
    run: BaseRun


class ManyRunsInResponse(RWModel):
    runs: List[BaseRun]
