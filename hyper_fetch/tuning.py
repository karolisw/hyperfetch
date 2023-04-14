from hyper_fetch.manager import Manager
from codecarbon import EmissionsTracker
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from hyper_fetch.util import get_yaml_val

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
            collection=collection,
            study_name=manager.name
        )


if __name__ == "__main__":
    asyncio.run(tune(config_path="../config/tuning_parameters.yml"))
