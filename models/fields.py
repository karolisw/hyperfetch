"""MODELS - FIELDS.
Fields used in the model classes as attributes.
"""

from pydantic import Field

# # Package # #
from utils.db_utils import get_uuid

__all__ = "RunFields"


class RunFields:
    run_id = Field(
        description="Unique identifier of this run in the database",
        example=get_uuid(),
        min_length=36,
        max_length=36
    )
    trial = Field(
        description="Best performing hyperparameters for the run"
    )
    name = Field(
        description="String concatation of environment name and algorithm name",
        example="LunarLander-v2_ppo"
    )
    energy_consumed = Field(
        description="The energy (kWh) consumed by the device that ran the run"
    )
    cpu_model = Field(
        description="The CPU model of the device",
        example="12th Gen Intel(R) Core(TM) i5-12500H"
    )
    gpu_model = Field(
        description="The GPU model of the device",
        example="Nvidia RTX 3070"
    )
    CO2_emissions = Field(
        description="The CO2 emissions caused by the device for the duration of the run"
    )
    alg = Field(
        description="The Reinforcement Learning algorithm (or agent) used in the environment",
        example="PPO"
    )
    env = Field(
        description="The environment that the agent interacts with",
        example="LunarLander-v2",
    )
    total_time = Field(
        description="The total time for the run/study from start to finish"
    )
    reward = Field(
        description="The best reward accomplished by the agent when training in the environment"
    )
