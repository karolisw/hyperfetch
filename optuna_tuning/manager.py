# type: ignore
import logging
import logging.config
from datetime import datetime
from pprint import pprint
import gym
import motor.motor_asyncio as motor
import optuna
import pandas as pd
import pymongo
import torch
from bson.json_util import dumps
from gym import spaces
from optuna.integration import SkoptSampler
from optuna.pruners import SuccessiveHalvingPruner, MedianPruner, NopPruner, HyperbandPruner, PercentilePruner, \
    PatientPruner, ThresholdPruner
from optuna.samplers import RandomSampler, GridSampler, TPESampler, CmaEsSampler, NSGAIISampler
from optuna.trial import FrozenTrial
from stable_baselines3 import PPO, DQN, A2C, TD3, SAC
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.preprocessing import is_image_space, is_image_space_channels_first
from stable_baselines3.common.vec_env import VecTransposeImage, is_vecenv_wrapped
from stable_baselines3.common.vec_env.vec_frame_stack import VecFrameStack
from utils.common import *
from optuna_tuning.alg_samplers import ALG_HP_SAMPLER
from optuna_tuning.callbacks import TrialEvalCallback, ThresholdExceeded

def _select_model(alg, **kwargs) :
    if alg == "ppo":
        return PPO(**kwargs)
    elif alg == "dqn":
        return DQN(**kwargs)
    elif alg == "a2c":
        return A2C(**kwargs)
    elif alg == "td3":
        return TD3(**kwargs)
    elif alg == "sac":
        return SAC(**kwargs)


class Manager:
    def __init__(self, config_path):
        '''
        :param config_path: Must be specified to avoid error

        '''
        self.start_time = datetime.now()
        self.end_time = datetime.now()
        self.config_path = config_path

        # Assigns values to most of the parameters above
        self._preprocess_args(config_path)

    def _create_callback(self, trial: optuna.Trial, log_path, eval_env):

        eval_freq_optuna = int(self.n_timesteps / self.n_evaluations)

        # Account for parallel envs
        eval_freq_optuna = max(eval_freq_optuna // self.n_envs, 1)

        # Callback that ends entire study if the run performs well enough for the user
        if self.reward_threshold is not None:

            # Callback for periodically evaluating and reporting performance.
            eval_callback = TrialEvalCallback(
                eval_env=eval_env, trial=trial, log_path=log_path, n_eval_episodes=self.n_evaluations,
                eval_freq=eval_freq_optuna, deterministic=True)
        else:
            # Without early stopping
            eval_callback = TrialEvalCallback(
                eval_env=eval_env, trial=trial, log_path=log_path, n_eval_episodes=self.n_evaluations,
                eval_freq=eval_freq_optuna, deterministic=True)

        return eval_callback

    def objective(self, trial: optuna.Trial) -> float:

        # Creating an environment for the model
        env = self.create_envs(n_envs=self.n_envs, no_log=True)

        # Essential args
        kwargs = {"policy": self.policy, "env": env, "seed": None}

        # Retrieving hyperparameters related to current algorithm
        hyperparameters = ALG_HP_SAMPLER[self.alg](trial)
        kwargs.update(hyperparameters)

        # Create the RL model
        model = _select_model(self.alg, **kwargs)

        # Creating evaluation env
        eval_env = self.create_envs(n_envs=self.n_envs, eval_env=True)

        # The user can state that the path is None in config to avoid logging
        path = None
        if self.trial_log_path is not None:
            path = os.path.join(self.trial_log_path, "trial_" + str(trial.number))

        # Dictionary of callbacks passed to learn method
        eval_callback = self._create_callback(trial=trial, log_path=path, eval_env=eval_env)

        try:
            model.learn(self.n_timesteps, callback=eval_callback)
            # Free memory
            model.env.close()
            eval_env.close()
        except (AssertionError, ValueError) as e:
            # Free memory
            model.env.close()
            eval_env.close()
            # Prune hyperparams that generate NaNs
            print(e)
            print("============")
            print("Sampled hyperparams:")
            pprint(hyperparameters)
            raise optuna.exceptions.TrialPruned()

        # Return the mean reward of the trial
        is_pruned = eval_callback.is_pruned
        reward = eval_callback.last_mean_reward

        del model.env, eval_env
        del model

        if is_pruned:
            raise optuna.exceptions.TrialPruned()

        return reward

    def run(self) -> FrozenTrial:

        def check_threshold(study: optuna.study, trial):
            try:
                if study.best_value > self.reward_threshold:
                    raise ThresholdExceeded()
            # ValueError in the start because there is no study.best value before any trials are run
            except ValueError:
                pass
            return

        # Set pytorch num threads to 1 for faster training.
        torch.set_num_threads(1)

        # Using config args, the sampler and pruner is selected
        # Select sampler and pruner and assign to self
        sampler = self._select_sampler()
        pruner = self._select_pruner()

        # Do not prune before 1/3 of the max budget is used.
        # pruner = MedianPruner(n_startup_trials=N_STARTUP_TRIALS, n_warmup_steps=N_EVALUATIONS // 3)

        study = optuna.create_study(sampler=sampler, pruner=pruner, study_name=self.name,
                                    direction="maximize")
        try:
            if self.reward_threshold is None:
                study.optimize(self.objective, n_jobs=self.n_jobs, n_trials=self.n_trials)  # , timeout=600)
            else:
                study.optimize(self.objective, n_jobs=self.n_jobs, n_trials=self.n_trials,
                               callbacks=[check_threshold])  # todo remove the reward threshold from here
        except ThresholdExceeded:
            print('Threshold exceeded: {} > {}'.format(study.best_value, self.reward_threshold))

        print("Number of finished trials: ", len(study.trials))

        trial = study.best_trial
        print("Best trial: ", trial)

        print("Value: ", trial.value)

        print("Params: ")
        for key, value in trial.params.items():
            print("    {}: {}".format(key, value))

        print("  User attrs:")
        for key, value in trial.user_attrs.items():
            print("    {}: {}".format(key, value))

        report_name = (
            f"report_{self.env}_{self.n_trials}-trials-{self.n_timesteps}"
            f"-{self.sampler}-{self.pruner}_{int(time())}"
        )
        # This is where the report will be written to
        log_path = os.path.join(self.log_folder, self.alg, report_name)
        self.logger.info("Writing report to %s", log_path)

        # Write report
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        study.trials_dataframe().to_csv(f"{log_path}.csv")

        # Save the end time of the run
        self.end_time = datetime.now()

        # Return the best trial
        return trial


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

    def _preprocess_args(self, path_to_config) -> None:
        if (not os.path.isfile(path_to_config)) or (not path_to_config.endswith('.yml')):
            logger.error("There is no .yml file at %s", path_to_config, stack_info=True)

        stream = open(path_to_config, 'r')
        data = yaml.safe_load(stream)  # dict

        if 'log_folder' not in data.keys():  # todo cannot log this here
            data.update({'log_folder': 'logs'})
            with open(path_to_config, "w") as writer:
                yaml.safe_dump(data, writer)

        # Create the logger and log folder (unless it exists)
        self.log_folder = data['log_folder']
        create_log_folder(self.log_folder)
        self._create_logger("test_logger")
        logger.info('Path to log folder: "{}"'.format(self.log_folder))

        if 'alg' not in data.keys():
            logger.error("An algorithm 'alg' must be specified in config at path %s",
                         path_to_config, stack_info=True)

        if 'env' not in data.keys():
            logger.error("An environment 'env' must be specified in config at path %s",
                         path_to_config, stack_info=True)

        policy_list = {"MlpPolicy", "CnnPolicy", "MultiInputPolicy"}
        if 'policy' not in data.keys() or 'policy' not in policy_list:
            logger.info('No policy was specified. Config value "policy" set to "MlpPolicy"')
            data.update({'policy': 'MlpPolicy'})
            with open(path_to_config, "w") as writer:
                yaml.safe_dump(data, writer)

        if 'reward_threshold' not in data.keys():
            logger.info('"reward_threshold" not specified. Callback for stopping on specified reward will not be used.')
            data.update({'reward_threshold': None})
            with open(path_to_config, "w") as writer:
                yaml.safe_dump(data, writer)

        if 'post_run' not in data.keys():
            logger.info('Whether or not to "post_run" was not specified. Config value "post_run" set to True.')
            data.update({'post_run': True})
            with open(path_to_config, "w") as writer:
                yaml.safe_dump(data, writer)

        if 'n_envs' not in data.keys():
            logger.info('No n_envs was specified. Config value "n_envs" set to 1.')
            data.update({'n_envs': 1})
            with open(path_to_config, "w") as writer:
                yaml.safe_dump(data, writer)

        if 'frame_stack' not in data.keys():
            logger.info('frame_stack not specified. Config value "frame_stack" set to "None".')
            data.update({'frame_stack': None})
            with open(path_to_config, "w") as writer:
                yaml.safe_dump(data, writer)

        # Used for finding elements in MongoDB -> name == env + alg
        if 'name' not in data.keys():
            # now = datetime.now()
            env = data['env']
            alg = data['alg']
            name = env + "_" + alg  # + "_" + now.strftime("%d/%m/%Y_%H:%M:%S")
            logger.info('No name was specified for the study. Config value "name" set to %s.', name)
            data.update({'name': name})
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

        if 'trial_log_path' not in data.keys():
            logger.info('No trial_log_path was specified. Config value "trial_log_path" set to "logs/trials".')
            data.update({'trial_log_path': 'logs/trials'})
            with open(path_to_config, "w") as writer:
                yaml.safe_dump(data, writer)

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

        if 'eval_freq' not in data.keys():
            logger.info('No eval_freq was specified for the eval callback. Config value "eval_freq" set to 10000.')
            data.update({'eval_freq': 10000})
            with open(path_to_config, "w") as writer:
                yaml.safe_dump(data, writer)

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
        self.policy = data['policy']
        self.reward_threshold = data['reward_threshold']
        self.post_run = data['post_run']
        self.n_envs = data['n_envs']
        self.frame_stack = data['frame_stack']
        self.name = data['name']
        self.sampler = data['sampler']
        self.pruner = data['pruner']
        self.seed = data['seed']
        self.n_startup_trials = data['n_startup_trials']
        self.trial_log_path = data['trial_log_path']
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
            self.min_resource = data['min_resource']
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

    def _select_sampler(self) -> optuna.samplers:
        """
        Recommended: random, tpe (default) or skopt
        return: Nothing, but assigns sampler to the Manager object
        """
        sampler = self.sampler
        seed = self.seed
        n_startup_trials = self.n_startup_trials

        # self.sampler changes from string to sampler object
        if sampler == "random":
            return RandomSampler(seed=seed)
        elif sampler == "cmaes":
            return CmaEsSampler(n_startup_trials=n_startup_trials, seed=seed)
        elif sampler == "nsgaii":
            return NSGAIISampler(population_size=self.population_size, mutation_prob=self.mutation_prob,
                                 crossover_prob=self.crossover_prob, swapping_prob=self.swapping_prob,
                                 seed=seed)
        elif sampler == "tpe":
            return TPESampler(n_startup_trials=n_startup_trials, seed=seed, multivariate=True)
        elif sampler == "skopt":
            return SkoptSampler(skopt_kwargs={"base_estimator": "GP", "acq_func": "gp_hedge"})
        else:
            logger.error("Unknown sampler %s", sampler, stack_info=True)

    def _select_pruner(self) -> optuna.pruners:
        pruner = self.pruner

        if pruner == "halving":
            return SuccessiveHalvingPruner()
        elif pruner == "median":
            return MedianPruner(n_startup_trials=self.n_startup_trials,
                                n_warmup_steps=self.n_evaluations // 3,
                                # interval_steps=self.eval_freq,
                                n_min_trials=self.n_min_trials)
        elif pruner == "patient":
            wrapped_pruner = MedianPruner(n_startup_trials=self.n_startup_trials,
                                          n_warmup_steps=self.n_evaluations // 3,
                                          # interval_steps=self.eval_freq,
                                          n_min_trials=self.n_min_trials)
            return PatientPruner(wrapped_pruner=wrapped_pruner,
                                 patience=self.patience,
                                 min_delta=self.min_delta)
        elif pruner == "percentile":
            return PercentilePruner(n_startup_trials=self.n_startup_trials,
                                    percentile=self.percentile,
                                    n_warmup_steps=self.n_evaluations // 3,
                                    # interval_steps=self.eval_freq,
                                    n_min_trials=self.n_min_trials)
        elif pruner == "hyperband":
            return HyperbandPruner(min_resource=self.min_resource,  # the number of halving-pruners
                                   max_resource=self.max_resource,
                                   reduction_factor=self.reduction_factor,
                                   bootstrap_count=self.bootstrap_count)
        elif pruner == "threshold":
            return ThresholdPruner(lower=self.lower,
                                   upper=self.upper,
                                   n_warmup_steps=self.n_evaluations // 3)
            # interval_steps=self.eval_freq)
        elif pruner == "none":
            return NopPruner()  # Do not prune

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

        spec = gym.spec(self.env)

        def make_env(**kwargs) -> gym.Env:
            gym_env = spec.make(**kwargs)
            return gym_env

        # On most env, SubprocVecEnv does not help and is quite memory hungry
        # therefore we use DummyVecEnv by default
        env = make_vec_env(
            make_env,
            n_envs=n_envs,
            # seed=self.seed,
            monitor_dir=log_dir
        )

        # Wrap the env into a VecNormalize wrapper if needed
        # and load saved statistics when present
        env = normalize_if_needed(env, eval_env)  # todo comment out if fails

        # Optional Frame-stacking
        if self.frame_stack is not None:
            n_stack = self.frame_stack
            env = VecFrameStack(env, n_stack)
            self.logger.info(f"Stacking {n_stack} frames")

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

    async def save_trial(self, trial, client, db, collection, study_name) -> None:

        # Creating connection
        my_client = motor.AsyncIOMotorClient(client)

        # Find the time spent running the algorithm
        duration = str(self.end_time - self.start_time)

        # Retrieve the most recent entry
        df = pd.read_csv('emissions.csv')
        last_row = df.iloc[-1]

        energy_consumed = last_row['energy_consumed']
        cpu_model = last_row['cpu_model']
        gpu_model = last_row['gpu_model']
        emissions = last_row['emissions']

        print("Creating dict...")

        run = {'_id': get_uuid(),
               'trial': trial.params,
                'name': study_name,
                'energy_consumed': energy_consumed,
                'cpu_model': cpu_model,
                'gpu_model': gpu_model,
                'CO2_emissions': emissions,
                'alg': self.alg,
                'env': self.env,
                'total_time': duration,
                'reward': trial.value}


        print("Posting...")

        await my_client[db][collection].insert_one(run)
        print("Posted!")


if __name__ == '__main__':
    manager = Manager(config_path="../config/tuning_parameters.yml")
    manager.run()
