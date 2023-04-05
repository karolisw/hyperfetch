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
        return True