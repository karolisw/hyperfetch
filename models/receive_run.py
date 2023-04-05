"""MODELS - PERSON - READ
Run Read model. Inherits from RunCreate and adds the run_id field, which is the _id field on Mongo documents
"""

from typing import List
import pydantic
from .create_run import RunCreate
from .fields import RunFields
from models.base_model import BaseModel

__all__ = ("RunRead", "RunsRead", "EnvRead", "EnvsRead")


class EnvRead(BaseModel):
    env: str = RunFields.env


class RunRead(RunCreate):
    """Body of Run GET and POST responses"""
    run_id: str = RunFields.run_id

    @pydantic.root_validator(pre=True)
    def _set_run_id(cls, data):
        """Swap the field _id to run_id"""
        document_id = data.get("_id")
        if document_id:
            data["run_id"] = document_id
        return data

    class Config(RunCreate.Config):
        extra = pydantic.Extra.ignore


RunsRead = List[RunRead]
EnvsRead = List[EnvRead]
