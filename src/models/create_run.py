"""
Run Create model. Inherits from PersonUpdate, but all the required fields must be re-defined
"""
from .fields import RunFields
from src.models.base_model import BaseModel
from typing import Dict,Union

__all__ = ("RunCreate",)


class RunCreate(BaseModel):
    """
    Body of Run POST request, but in reality it functions as a base class,
    as other Pydantic classes inherit from this class.
    """
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
    sampler: str = RunFields.sampler
    pruner: str = RunFields.pruner
    n_trials: str = RunFields.n_trials
    country: str = RunFields.country
    region: str = RunFields.region
    cloud_provider: str = RunFields.cloud_provider
    cloud_region: str = RunFields.cloud_region
    os: str = RunFields.os
    python_version: str = RunFields.python_version
