import argparse
from .manager import Manager
from codecarbon import EmissionsTracker
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

storage = "mongodb://localhost:27017/runs?authSource=admin"
db = "runs"
collection = "run"

client = AsyncIOMotorClient(storage)

# Tracks emissions (writes to emissions.csv)
tracker = EmissionsTracker()


def tune() -> None:
    """
    :return: Nothing is returned. Results from trials are written to log-folder.
             Best hyperparameters are written to console for the user to see.
    """
    parser = argparse.ArgumentParser(description='"tune" script allows for tuning hyperparameters '
                                                 'in HyperFetch. Hyperparameters are also persisted unless'
                                                 '"post_run" is explicitly configured as "false" in config file.')
    parser.add_argument('config_path', type=str, help='The path to the config file (.yaml).')

    args = parser.parse_args()

    tracker.start()
    manager = Manager(config_path=args.config_path)

    # Best performing trial is returned as FrozenTrial
    best_trial = manager.run()

    tracker.stop()

    # Post trial along with the tracking data unless user's config file states not to
    if manager.post_run:
        asyncio.run(manager.save_trial(
            trial=best_trial,
            client=storage,
            db=db,
            collection=collection
        ))


def save() -> None:
    """
    Method that allows researchers/developers/students to persist their hyperparameters.
    This method is only for posting hyperparameters that have not been tuned using
    HyperFetch. Thus, there is no way of posting reward alongside these hyperparameters
    as the reward cannot be validated by HyperFetch. However, the user must still add
    project_name and git_link to config file; and there is nothing in the way of posting
    the reward there (git).
    :return: Nothing is returned. The hyperparameters are posted.
    """
    parser = argparse.ArgumentParser(description='"save" script allows for persisting hyperparameters that are not '
                                                 'tuned in HyperFetch.')
    parser.add_argument('config_path', type=str, help='The path to the config file (.yaml). Can be a new file or t'
                                                      'he same as for the tuning() method.')

    args = parser.parse_args()
    manager = Manager(config_path=args.config_path)
    asyncio.run(manager.save_custom(client=storage, db=db, collection=collection))
