import os

import yaml
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
