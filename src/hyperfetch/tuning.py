import argparse
from .manager import Manager
from codecarbon import EmissionsTracker
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from .auth_connection import MONGODB_URL, MONGO_DB, MONGO_COLLECTION

client = AsyncIOMotorClient(MONGODB_URL)

# Tracks emissions (writes to emissions.csv)
tracker = EmissionsTracker()


def tune(config_path: str) -> None:

    """
    Tune hyperparameters for alg/env combo specified in config path.
    This method is not for the command line, but for use inside scripts.
    :param config_path: The path to config file. To read full config documentation,
                  read the project/PyPi README to set up the front -and backend
                  such that you can run the website.
    :return: Nothing is returned. Results from trials are written to log-folder.
             Best hyperparameters are written to console for the user to see.
    """

    tracker.start()
    manager = Manager(config_path=config_path)

    # Best performing trial is returned as FrozenTrial
    best_trial = manager.run()

    tracker.stop()

    # Post trial along with the tracking data unless user's config file states not to
    if manager.post_run:
        asyncio.run(manager.save_trial(
            trial=best_trial,
            client=MONGODB_URL,
            db=MONGO_DB,
            collection=MONGO_COLLECTION
        ))


def save(config_path: str) -> None:
    """
    Method that allows researchers/developers/students to persist their hyperparameters.
    This method is only for posting hyperparameters that have not been tuned using
    HyperFetch. Thus, there is no way of posting reward alongside these hyperparameters
    as the reward cannot be validated by HyperFetch. However, the user must still add
    project_name and git_link to config file; and there is nothing in the way of posting
    the reward there (git).
    :param config_path: The path to config file. To read full config documentation,
              read the project/PyPi README to set up the front -and backend
              such that you can run the website.
    :return: Nothing is returned. The hyperparameters are posted.
    """

    manager = Manager(config_path=config_path)
    asyncio.run(manager.save_custom(client=MONGODB_URL, db=MONGO_DB, collection=MONGO_COLLECTION))


def tune_cli() -> None:
    """
    Tune hyperparameters for alg/env combo specified in congig file with path
    specified as a command line argument.
    This method is not for use inside scripts, but for use in the command line.

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
            client=MONGODB_URL,
            db=MONGO_DB,
            collection=MONGO_COLLECTION
        ))


def save_cli() -> None:
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
    asyncio.run(manager.save_custom(client=MONGODB_URL, db=MONGO_DB, collection=MONGO_COLLECTION))
