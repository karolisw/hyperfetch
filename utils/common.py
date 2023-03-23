import os
from typing import Dict

import yaml
from collections.abc import Iterable
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.openapi.constants import REF_PREFIX
from fastapi.openapi.utils import (
    validation_error_definition,
    validation_error_response_definition,
)
from starlette.exceptions import HTTPException
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY
from stable_baselines3.common.vec_env import VecEnv, VecNormalize
from time import time
from uuid import uuid4
from typing import Union

def get_time(seconds_precision=True) -> Union[int, float]:
    """Returns the current time as Unix/Epoch timestamp, seconds precision by default"""
    return time() if not seconds_precision else int(time())


def get_uuid() -> str:
    """Returns an unique UUID (UUID4)"""
    return str(uuid4())
def get_yaml_val(config_path: str, key: str) -> str:
    stream = open(config_path, 'r')
    data = yaml.safe_load(stream)
    return data[key]


def normalize_if_needed(env: VecEnv, eval_env: bool) -> VecEnv:
    # In eval env: turn off reward normalization and normalization stats updates.
    if eval_env:
        env = VecNormalize(env, norm_reward=False, training=False)
    else:
        env = VecNormalize(env)
    return env


# Creates directory in config-specified folder if it does not already exist.
def create_log_folder(path: str) -> None:
    os.makedirs(path, exist_ok=True)


async def http_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse({"errors": [exc.detail]})


async def http_422_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handler for 422 error to transform default pydantic error object to gothinkster format
    """

    errors: Dict[str, list] = {"body": []}

    if isinstance(exc.detail, Iterable) and not isinstance(
        exc.detail, str
    ):  # check if error is pydantic's model error
        for error in exc.detail:
            error_name = ".".join(
                error["loc"][1:]
            )  # remove 'body' from path to invalid element
            errors["body"].append({error_name: error["msg"]})
    else:
        errors["body"].append(exc.detail)

    return JSONResponse({"errors": errors}, status_code=HTTP_422_UNPROCESSABLE_ENTITY)

validation_error_definition["properties"] = {
    "body": {"title": "Body", "type": "array", "items": {"type": "string"}}
}

validation_error_response_definition["properties"] = {
    "errors": {
        "title": "Errors",
        "type": "array",
        "items": {"$ref": REF_PREFIX + "ValidationError"},
    }
}
