import optuna
from typing import Optional
from stable_baselines3.common.callbacks import BaseCallback, EvalCallback, StopTrainingOnRewardThreshold
from stable_baselines3.common.logger import TensorBoardOutputFormat
from stable_baselines3.common.vec_env import VecEnv


class ThresholdExceeded(optuna.exceptions.OptunaError):
    pass


def check_threshold(study: optuna.study, trial, reward_threshold):
    try:
        if study.best_value < reward_threshold:
            raise ThresholdExceeded()
    # ValueError in the start because there is no study.best value before any trials are run
    except ValueError:
        pass
    return


class EarlyStoppingCallback(StopTrainingOnRewardThreshold):
    def __init__(
            self,
            reward_threshold: int,
            trial: optuna.Trial,
            verbose: int = 0,
    ) -> None:
        super().__init__(
            reward_threshold=reward_threshold,
            verbose=verbose
        )
        self.trial = trial

    def _on_step(self) -> bool:
        # continue_training = super()._on_step()
        continue_training = self.trial.study.best_trial.value < self.reward_threshold  # true when best value smaller than reward threshold
        # If the reward is good enough, the whole study stops
        if not continue_training:
            print("trying to stop trial")
            self.trial.study.stop()
            return False

        return True


class TrialEvalCallback(EvalCallback):
    """
    Callback used for evaluating and reporting a trial.
    """

    def __init__(
            self,
            eval_env: VecEnv,  # or gym.Env
            trial: optuna.Trial,
            n_eval_episodes: int = 5,
            eval_freq: int = 10000,
            deterministic: bool = True,
            verbose: int = 0,
            best_model_save_path: Optional[str] = None,
            log_path: Optional[str] = None,
            callback_on_new_best=None,
            reward_threshold=None

    ) -> None:
        super().__init__(
            eval_env=eval_env,
            n_eval_episodes=n_eval_episodes,
            eval_freq=eval_freq,
            deterministic=deterministic,
            verbose=verbose,
            best_model_save_path=best_model_save_path,
            log_path=log_path
            # callback_on_new_best=callback_on_new_best
        )
        self.trial = trial
        self.eval_idx = 0
        self.is_pruned = False
        # self.reward_threshold = reward_threshold

    def _on_step(self) -> bool:
        if self.eval_freq > 0 and self.n_calls % self.eval_freq == 0:
            super()._on_step()
            self.eval_idx += 1
            # Report the mean reward to optuna
            self.trial.report(self.last_mean_reward, self.eval_idx)
            # Prune trial if the last_mean_reward was underperforming
            if self.trial.should_prune():
                self.is_pruned = True
                return False
            '''
            elif self.reward_threshold is not None:
                # Early stop if reward threshold reached
                print("best value: ", self.trial.study.best_value)
                if self.trial.study.best_value > self.reward_threshold:
                    self.trial.study.stop() #todo could work if i pass study instead of trial?
                    return False
            '''
        return True


class RawStatisticsCallback(BaseCallback):
    """
    Callback used for logging raw episode data (return and episode length).
    """

    def __init__(self, verbose=0):
        super().__init__(verbose)
        # Custom counter to reports stats
        # (and avoid reporting multiple values for the same step)
        self._timesteps_counter = 0
        self._tensorboard_writer = None

    def _init_callback(self) -> None:
        assert self.logger is not None
        # Retrieve tensorboard writer to not flood the logger output
        for out_format in self.logger.output_formats:
            if isinstance(out_format, TensorBoardOutputFormat):
                self._tensorboard_writer = out_format
        assert self._tensorboard_writer is not None, \
            "You must activate tensorboard logging when using RawStatisticsCallback"

    def _on_step(self) -> bool:
        for info in self.locals["infos"]:
            if "episode" in info:
                logger_dict = {
                    "raw/rollouts/episodic_return": info["episode"]["r"],
                    "raw/rollouts/episodic_length": info["episode"]["l"],
                }
                exclude_dict = {key: None for key in logger_dict.keys()}
                self._timesteps_counter += info["episode"]["l"]
                self._tensorboard_writer.write(logger_dict, exclude_dict, self._timesteps_counter)

        return True
