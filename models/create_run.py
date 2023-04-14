"""
Run Create model. Inherits from PersonUpdate, but all the required fields must be re-defined
"""
from .fields import RunFields
from models.base_model import BaseModel
from typing import Dict,Union

__all__ = ("RunCreate",)


class RunCreate(BaseModel):
    """Body of Run POST request"""
    trial: Dict[str, Union[str, float]] = RunFields.trial
    project_name: str = RunFields.project_name
    git_link: str = RunFields.git_link
    energy_consumed: float = RunFields.energy_consumed
    cpu_model: str = RunFields.cpu_model
    gpu_model: str = RunFields.gpu_model
    CO2_emissions: float = RunFields.CO2_emissions
    alg: str = RunFields.alg
    env: str = RunFields.env
    total_time: str = RunFields.total_time
    reward: float = RunFields.reward
