from hyperfetch.manager import Manager
from codecarbon import EmissionsTracker
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from hyperfetch.util import get_yaml_val

storage = get_yaml_val("../config/no_auth_connection.yml", "url")
db = get_yaml_val("../config/no_auth_connection.yml", "db")
collection = get_yaml_val("../config/no_auth_connection.yml", "collection")

client = AsyncIOMotorClient(storage)

# Tracks emissions (writes to emissions.csv)
tracker = EmissionsTracker()


async def tune(config_path) -> None:
    """
    :param config_path: Path to configuration file (.yml).
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
        await manager.save_trial(
            trial=best_trial,
            client=storage,
            db=db,
            collection=collection
        )


async def save_custom_parameters(config_path: str) -> None:
    """
    Method that allows researchers/developers/students to persist their hyperparameters.
    This method is only for posting hyperparameters that have not been tuned using
    HyperFetch. Thus, there is no way of posting reward alongside these hyperparameters
    as the reward cannot be validated by HyperFetch. However, the user must still add
    project_name and git_link to config file; and there is nothing in the way of posting
    the reward there (git).
    :param config_path: The path to the config file (.yaml). Can be a new file or the same
                        as for the tuning() method.
    :return: Nothing is returned. The hyperparameters are posted.
    """
    manager = Manager(config_path=config_path)
    await manager.save_custom(client=storage, db=db, collection=collection)


if __name__ == "__main__":
    #asyncio.run(save_custom_parameters(config_path="../config/tuning_parameters.yml"))
    asyncio.run(tune(config_path="../config/tuning_parameters.yml"))
