import os

import yaml
from stable_baselines3.common.vec_env import VecEnv, VecNormalize


def get_yaml_val(config_path, key) -> str:
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
def create_log_folder(path) -> None:
    os.makedirs(path, exist_ok=True)
