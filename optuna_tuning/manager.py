import os
from typing import Optional

import optuna
import yaml
import logging
import logging.config

import gymnasium as gym
from gymnasium import spaces
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.preprocessing import is_image_space, is_image_space_channels_first
from stable_baselines3.common.vec_env import VecTransposeImage, is_vecenv_wrapped, VecNormalize
from stable_baselines3.common.vec_env.base_vec_env import VecEnv
from stable_baselines3.common.vec_env.vec_frame_stack import VecFrameStack

from datetime import datetime
from optuna.samplers import RandomSampler, GridSampler, TPESampler, CmaEsSampler, NSGAIISampler
from optuna.integration import SkoptSampler
from optuna.pruners import SuccessiveHalvingPruner, MedianPruner, NopPruner, HyperbandPruner, PercentilePruner, \
    PatientPruner, ThresholdPruner
from alg_samplers import ALG_HP_SAMPLER

logger: Optional[logging.Logger] = None  # logger configured during init()


# TODO part of init() and all other functions here are part of the manager
class Manager:
    def __init__(self, log_folder, config_path="hp_config.yml"
                                               """,
        # Assigned through the use of config file "hp_config.yml"
        alg,
        env,
        name,
        sampler,
        pruner,
        seed,
        n_startup_trials,
        n_timesteps,
        n_jobs,
        n_evaluations,
        eval_freq,
        n_trials,
        n_warmup_steps,
        n_min_trials,
        log_folder,
        # Assigned through the use of "_pruner_check"
        patience,
        min_delta,
        percentile,
        max_resource,
        min_resource,
        reduction_factor,
        bootstrap_count,
        upper,
        lower,
        # Assigned through the use of "_sampler_check"
        population_size,
        mutation_prob,
        crossover_prob,
        swapping_prob,
        # Assigned through the use of "alg_samplers.py"
        """
                 ):
        # Does not create a new folder if the folder already exists
        self.log_folder = log_folder
        _create_log_folder(self.log_folder)

        self._create_logger("test_logger")

        # Assigns values to most of the parameters above
        self._verify_config(config_path)

        print("env: ", self.env)
        print("alg: ", self.alg)
        print("name: ", self.name)
        print("sampler: ", self.sampler)
        print("pruner: ", self.pruner)
        print("seed: ", self.seed)
        print("n_startup_trials: ", self.n_startup_trials)
        print("n_trials: ", self.n_trials)

        # TODO create env
        # TODO create model
        # TODO assign policy to hp_config and add it to verify config

    def objective(self, trial: optuna.Trial) -> float:
        # Retrieving hyperparameters related to current algorithm
        kwargs = ALG_HP_SAMPLER[self.alg](trial)
        # Updating with current
        kwargs.update({"policy": "MlpPolicy", "env": self.env})  # todo write self.policy when self has a policy

    def _create_logger(self, logger_name) -> None:
        """
        :param logger_name: name of the logger
        :return: None, but sets the global logger object
        """

        global logger
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.INFO)

        # Create handlers
        c_handler = logging.StreamHandler()
        f_handler = logging.FileHandler(self.log_folder + "/error.log")
        c_handler.setLevel(logging.INFO)
        f_handler.setLevel(logging.ERROR)

        # Create formatters and add it to the handlers
        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

        # Add to self
        self.logger = logger

    def _verify_config(self, path_to_config) -> None:
        if (not os.path.isfile(path_to_config)) or (not path_to_config.endswith('.yml')):
            logger.error("There is no .yml file at %s", path_to_config, stack_info=True)

        stream = open(path_to_config, 'r')
        data = yaml.safe_load(stream)  # dict

        if 'alg' not in data.keys():
            logger.error("An algorithm 'alg' must be specified in config at path %s",
                         path_to_config, stack_info=True)

        if 'env' not in data.keys():
            logger.error("An environment 'env' must be specified in config at path %s",
                         path_to_config, stack_info=True)

        if 'name' not in data.keys():
            now = datetime.now()
            dt_string = 'study_' + now.strftime("%d/%m/%Y_%H:%M:%S")
            logger.info('No name was specified for the study. Config value "name" set to %s.', dt_string)
            data.update({'name': dt_string})
            with open(path_to_config, "w") as writer:
                yaml.safe_dump(data, writer)

        if 'sampler' not in data.keys():
            logger.info('No sampler was specified. Config value "sampler" set to "tpe" (TPESampler).')
            data.update({'sampler': 'tpe'})
            with open(path_to_config, "w") as writer:
                yaml.safe_dump(data, writer)

        if 'pruner' not in data.keys():
            logger.info('No pruner was specified. Config value "tuner" set to "hyperband" (HyperbandTuner).')
            data.update({'pruner': 'hyperband'})
            with open(path_to_config, "w") as writer:
                yaml.safe_dump(data, writer)

        if 'seed' not in data.keys():
            logger.info('No seed was specified. Config value "seed" set to 0.')
            data.update({'seed': 0})
            with open(path_to_config, "w") as writer:
                yaml.safe_dump(data, writer)

        if 'n_startup_trials' not in data.keys():
            logger.info('No n_startup_trials was specified. Config value "n_startup_trials" set to 0.')
            data.update({'n_startup_trials': 0})
            with open(path_to_config, "w") as writer:
                yaml.safe_dump(data, writer)

        if 'log_folder' not in data.keys():
            logger.info('No log_folder was specified. Config value "log_folder" set to "logs".')
            data.update({'log_folder': 'logs'})
            with open(path_to_config, "w") as writer:
                yaml.dump(data, writer)

        if 'n_timesteps' not in data.keys():
            logger.info('No n_timesteps was specified. Config value "n_timesteps" set to 20000.')
            data.update({'n_timesteps': 20000})
            with open(path_to_config, "w") as writer:
                yaml.safe_dump(data, writer)

        if 'n_evaluations' not in data.keys():
            logger.info('No n_evaluations was specified. Config value "n_evaluations" set to 2.')
            data.update({'n_evaluations': 2})
            with open(path_to_config, "w") as writer:
                yaml.safe_dump(data, writer)

        if 'n_jobs' not in data.keys():
            logger.info('No n_jobs was specified. Config value "n_jobs" set to 1.')
            data.update({'n_jobs': 1})
            with open(path_to_config, "w") as writer:
                yaml.safe_dump(data, writer)

        if 'eval_freq' not in data.keys() or (
                'eval_freq' in data.keys() and data['eval_freq'] != (data['n_timesteps'] / data['n_evaluations'])):
            data.update({'eval_freq': int(data['n_timesteps'] / data['n_evaluations'])})
            with open(path_to_config, "w") as writer:
                yaml.safe_dump(data, writer)
            logger.info('eval_freq should be n_timesteps/n_evaluations. Config value "eval_freq" set to %s.',
                        data['eval_freq'])

        if 'n_trials' not in data.keys():
            logger.info('No n_trials was specified. Config value "n_trials" set to 500.')
            data.update({'n_trials': 500})
            with open(path_to_config, "w") as writer:
                yaml.safe_dump(data, writer)

        if 'n_warmup_steps' not in data.keys():
            logger.info('No n_warmup_steps was specified. Config value "n_warmup_steps" set to 0.')
            data.update({'n_warmup_steps': 0})
            with open(path_to_config, "w") as writer:
                yaml.safe_dump(data, writer)

        if 'n_min_trials' not in data.keys():
            logger.info('No n_min_trials was specified. Config value "n_min_trials" set to 1.')
            data.update({'n_min_trials': 1})
            with open(path_to_config, "w") as writer:
                yaml.safe_dump(data, writer)

        # Assign the now verified parameters to the Manager
        self.alg = data['alg']
        self.env = data['env']
        self.name = data['name']
        self.sampler = data['sampler']
        self.pruner = data['pruner']
        self.seed = data['seed']
        self.n_startup_trials = data['n_startup_trials']
        self.log_folder = data['log_folder']
        self.n_timesteps = data['n_timesteps']
        self.n_jobs = data['n_jobs']
        self.n_evaluations = data['n_evaluations']
        self.eval_freq = data['eval_freq']
        self.n_trials = data['n_trials']
        self.n_warmup_steps = data['n_warmup_steps']
        self.n_min_trials = data['n_min_trials']

        # Verify the pruner in separate method
        self._pruner_check(path_to_config)
        self._sampler_check(path_to_config)

    # Supporting method to the '_verify_config' method
    def _pruner_check(self, path_to_config) -> None:

        stream = open(path_to_config, 'r')
        data = yaml.safe_load(stream)  # dict

        if data['pruner'] == 'patient':
            # requires patience and min_delta
            if 'patience' not in data.keys():
                logger.info('Pruner is PatientPruner, but patience is not specified. '
                            'Config value "patience" set to 50')
                data.update({'patience': 50})
                with open(path_to_config, "w") as writer:
                    yaml.safe_dump(data, writer)
            if 'min_delta' not in data.keys():
                logger.info('Pruner is PatientPruner, but min_delta is not specified. '
                            'Config value "min_delta" set to 0.05')
                data.update({'min_delta': 0.05})
                with open(path_to_config, "w") as writer:
                    yaml.safe_dump(data, writer)
            elif data['min_delta'] < 0:
                logger.info(
                    'min_delta was specified, but should be a positive floating point number. '
                    'Config value "min_delta" set to 0.05.')
                data.update({'min_Delta': 0.05})
                with open(path_to_config, "w") as writer:
                    yaml.safe_dump(data, writer)
            self.patience = data['patience']
            self.min_delta = data['min_delta']

        elif data['pruner'] == 'percentile':
            if 'percentile' not in data.keys():
                logger.info('Pruner is PercentilePruner, but percentile is not specified. '
                            'Config value "percentile" set to 25.0')
                data.update({'percentile': 25.0})
                with open(path_to_config, "w") as writer:
                    yaml.safe_dump(data, writer)
            elif data['percentile'] < 0 or data['percentile'] > 100:
                logger.info('percentile was specified, but should be a positive floating point number '
                            'between 0 and 100. Config value "percentile" set to 25.0.')
                data.update({'percentile': 25.0})
                with open(path_to_config, "w") as writer:
                    yaml.safe_dump(data, writer)
            self.percentile = data['percentile']

        elif data['pruner'] == 'hyperband':
            if 'max_resource' not in data.keys():
                logger.info('Pruner is HyperbandPruner, but max_resource is not specified. '
                            'Config value "max_resource" set to "auto".')
                data.update({'max_resource': 'auto'})
                with open(path_to_config, "w") as writer:
                    yaml.safe_dump(data, writer)
            if 'min_resource' not in data.keys():
                logger.info('Pruner is HyperbandPruner, but min_resource is not specified. '
                            'Config value "min_resource" set to 1.')
                data.update({'min_resource': 1})
                with open(path_to_config, "w") as writer:
                    yaml.safe_dump(data, writer)
            if 'reduction_factor' not in data.keys():
                logger.info(
                    'Pruner is HyperbandPruner, but reduction_factor is not specified. '
                    'Config value "reduction_factor" set to 3.0.')
                data.update({'reduction_factor': 3.0})
                with open(path_to_config, "w") as writer:
                    yaml.safe_dump(data, writer)
            if 'bootstrap_count' not in data.keys():
                logger.info('Pruner is HyperbandPruner, but bootstrap_count is not specified. '
                            'Config value "bootstrap_count" set to 0.')
                data.update({'bootstrap_count': 0})
                with open(path_to_config, "w") as writer:
                    yaml.safe_dump(data, writer)
            self.max_resource = data['max_resource']
            self.min_resource = data['min_delta']
            self.reduction_factor = data['reduction_factor']
            self.bootstrap_count = data['bootstrap_count']

        elif data['pruner'] == 'threshold':
            if 'upper' not in data.keys():
                logger.info('Pruner is ThresholdPruner, but upper is not specified. '
                            'Config value "upper" set to 1.0')
                data.update({'upper': 1.0})
                with open(path_to_config, "w") as writer:
                    yaml.safe_dump(data, writer)
            if 'lower' not in data.keys():
                logger.info('Pruner is ThresholdPruner, but min_resource is not specified. '
                            'Config value "lower" set to 0.0')
                data.update({'lower': 0.0})
                with open(path_to_config, "w") as writer:
                    yaml.safe_dump(data, writer)
            self.upper = data['upper']
            self.lower = data['lower']

    # These checks are called before _create_sampler and _create_pruner
    def _sampler_check(self, path_to_config) -> None:

        stream = open(path_to_config, 'r')
        data = yaml.safe_load(stream)  # dict

        if data['sampler'] == 'nsgaii':
            if 'population_size' not in data.keys():
                logger.info('Sampler is NSGAIISampler, but population_size is not specified. '
                            'Config value "population_size" set to 50')
                data.update({'population_size': 50})
                with open(path_to_config, "w") as writer:
                    yaml.safe_dump(data, writer)
            if 'mutation_prob' not in data.keys():
                logger.info('Sampler is NSGAIISampler, but mutation_prob is not specified. '
                            'Config value "mutation_prob" set to 0.01')
                data.update({'mutation_prob': 0.01})
                with open(path_to_config, "w") as writer:
                    yaml.safe_dump(data, writer)
            if 'crossover_prob' not in data.keys():
                logger.info('Sampler is NSGAIISampler, but crossover_prob is not specified. Config value '
                            '"crossover_prob" set to 0.9')
                data.update({'crossover_prob': 0.9})
                with open(path_to_config, "w") as writer:
                    yaml.safe_dump(data, writer)
            if 'swapping_prob' not in data.keys():
                logger.info('Sampler is NSGAIISampler, but swapping_prob is not specified. '
                            'Config value "swapping_prob" set to 0.5')
                data.update({'swapping_prob': 0.5})
                with open(path_to_config, "w") as writer:
                    yaml.safe_dump(data, writer)
            self.population_size = data['population_size']
            self.mutation_prob = data['mutation_prob']
            self.crossover_prob = data['crossover_prob']
            self.swapping_prob = data['swapping_prob']

        if data['sampler'] == 'skopt':
            self.skopt_kwargs = {"base_estimator": "GP", "acq_func": "gp_hedge"}

    def _select_sampler(self) -> None:
        """
        Recommended: random, tpe (default) or skopt
        return: Nothing, but assigns sampler to the Manager object
        """
        sampler = self.sampler
        seed = self.seed
        n_startup_trials = self.n_startup_trials

        # self.sampler changes from string to sampler object
        if sampler == "random":
            self.sampler = RandomSampler(seed=seed)
        elif sampler == "grid":
            alg = self.alg
            # TODO GridSampler does not work because missing trial arg in parentheses () after [alg]
            self.sampler = GridSampler(search_space=ALG_HP_SAMPLER[alg](), seed=seed)
        elif sampler == "cmaes":
            self.sampler = CmaEsSampler(n_startup_trials=n_startup_trials, seed=seed)
        elif sampler == "nsgaii":
            self.sampler = NSGAIISampler(population_size=self.population_size, mutation_prob=self.mutation_prob,
                                         crossover_prob=self.crossover_prob, swapping_prob=self.swapping_prob,
                                         seed=seed)
        elif sampler == "tpe":
            self.sampler = TPESampler(n_startup_trials=n_startup_trials, seed=seed, multivariate=True)
        elif sampler == "skopt":
            self.sampler = SkoptSampler(skopt_kwargs={"base_estimator": "GP", "acq_func": "gp_hedge"})
        else:
            logger.error("Unknown sampler %s", sampler, stack_info=True)

    def _select_pruner(self) -> None:
        pruner = self.pruner

        if pruner == "halving":
            self.pruner = SuccessiveHalvingPruner()
        elif pruner == "median":
            self.pruner = MedianPruner(n_startup_trials=self.n_startup_trials,
                                       n_warmup_steps=self.n_warmup_steps,
                                       interval_steps=self.eval_freq,  # todo is this checked for in verification?
                                       n_min_trials=self.n_min_trials)
        elif pruner == "patient":
            wrapped_pruner = MedianPruner(n_startup_trials=self.n_startup_trials,
                                          n_warmup_steps=self.n_warmup_steps,
                                          interval_steps=self.eval_freq,
                                          n_min_trials=self.n_min_trials)
            self.pruner = PatientPruner(wrapped_pruner=wrapped_pruner,
                                        patience=self.patience,
                                        min_delta=self.min_delta)
        elif pruner == "percentile":
            self.pruner = PercentilePruner(n_startup_trials=self.n_startup_trials,
                                           percentile=self.percentile,
                                           n_warmup_steps=self.n_warmup_steps,
                                           interval_steps=self.eval_freq,
                                           n_min_trials=self.n_min_trials)
        elif pruner == "hyperband":
            self.pruner = HyperbandPruner(min_resource=self.min_resource,  # the number of halving-pruners
                                          max_resource=self.max_resource,
                                          reduction_factor=self.reduction_factor,
                                          bootstrap_count=self.bootstrap_count)
        elif pruner == "threshold":
            self.pruner = ThresholdPruner(lower=self.lower,
                                          upper=self.upper,
                                          n_warmup_steps=self.n_warmup_steps,
                                          interval_steps=self.eval_freq)
        elif pruner == "none":
            self.pruner = NopPruner()  # Do not prune

        else:
            logger.error("Unknown pruner %s", pruner, stack_info=True)

    def create_envs(self, n_envs: int, eval_env: bool = False, no_log: bool = False) -> VecEnv:
        """
        Create the environment and wrap it if necessary.
        :param self:
        :param n_envs:
        :param eval_env: Whether is it an environment used for evaluation or not
        :param no_log: Do not log training when doing hyperparameter optim
            (issue with writing the same file)
        :return: the vectorized environment, with appropriate wrappers
        """
        # Do not log eval env (issue with writing the same file)
        log_dir = None if eval_env or no_log else self.log_folder
        '''
        # Special case for GoalEnvs: log success rate too
        if (
                "Neck" in self.env
                or self.is_robotics_env(self.env_name.gym_id)
                or "parking-v0" in self.env_name.gym_id
                and len(self.monitor_kwargs) == 0  # do not overwrite custom kwargs
        ):
            self.monitor_kwargs = dict(info_keywords=("is_success",))
        '''

        spec = gym.spec(self.name)
        print("this is what gym spec looks like (line 457 atm): ", spec)

        '''
        def make_env(**kwargs) -> gym.Env:
            env = spec.make(**kwargs)
            return env
        '''

        # On most env, SubprocVecEnv does not help and is quite memory hungry
        # therefore we use DummyVecEnv by default
        env = make_vec_env(
            self.env,
            n_envs=n_envs,
            seed=self.seed,
            monitor_dir=log_dir,
        )

        # Wrap the env into a VecNormalize wrapper if needed
        # and load saved statistics when present
        env = _normalize_if_needed(env, eval_env)

        # Optional Frame-stacking
        if self.frame_stack is not None:
            n_stack = self.frame_stack
            env = VecFrameStack(env, n_stack)
            if self.verbose > 0:
                print(f"Stacking {n_stack} frames")

        if not is_vecenv_wrapped(env, VecTransposeImage):
            wrap_with_vec_transpose = False
            if isinstance(env.observation_space, spaces.Dict):
                # If even one of the keys is an image-space in need of transpose, apply transpose
                # If the image spaces are not consistent (for instance one is channel first,
                # the other channel last), VecTransposeImage will throw an error
                for space in env.observation_space.spaces.values():
                    wrap_with_vec_transpose = wrap_with_vec_transpose or (
                            is_image_space(space) and not is_image_space_channels_first(space)
                    )
            else:
                wrap_with_vec_transpose = is_image_space(env.observation_space) and not is_image_space_channels_first(
                    env.observation_space
                )

            if wrap_with_vec_transpose:
                logger.info("Wrapping the env in a VecTransposeImage.")
                env = VecTransposeImage(env)

        return env


def _normalize_if_needed(env: VecEnv, eval_env: bool) -> VecEnv:
    # In eval env: turn off reward normalization and normalization stats updates.
    if eval_env:
        env = VecNormalize(env, norm_reward=False, training=False)
    else:
        env = VecNormalize(env)
    return env


def _get_yaml_val(key) -> None:
    path = 'hp_config.yml'
    stream = open(path, 'r')
    data = yaml.safe_load(stream)
    # TODO add an if sentence for if the key is 'metric' because it is a dictionary -> discard metric if not needed
    return data[key]


# Creates directory in config-specified folder if it does not already exist.
def _create_log_folder(path) -> None:
    os.makedirs(path, exist_ok=True)


def objective():
    pass


def hyperparameter_optimization():
    pass


if __name__ == '__main__':
    #################### All these below should be added to the init() method ######################

    # _create_logger("hp_logger", log_path + "/file.log")
    # sampler = _create_sampler()
    # print(sampler)
    # pruner = _create_pruner()
    # print(pruner)
    # _verify_config("hp_config.yml")
    manager = Manager(log_folder="logs", config_path="hp_config.yml")
