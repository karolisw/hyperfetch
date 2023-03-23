from optuna_tuning.manager import Manager
from codecarbon import EmissionsTracker
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import config.core as core
from utils.common import get_yaml_val

storage = get_yaml_val("../config/db_config.yml", "url")
db = get_yaml_val("../config/db_config.yml", "db")
collection = get_yaml_val("../config/db_config.yml", "collection")

client = AsyncIOMotorClient(storage)


# Tracks electricity usage in kWh (writes to emissions.csv)
tracker = EmissionsTracker()

async def tune(log_folder, config_path):
    print("storage: ", storage)
    print("db: ", db)
    print("collection: ", collection)
    # Starts tracking electricity usage here
    tracker.start()

    manager = Manager(config_path=config_path)

    # Best performing trial is returned as FrozenTrial
    best_trial = manager.run()

    # Tracking ends here
    tracker.stop()

    # Post trial along with the tracking data if the user wishes to
    if manager.post_run:
        await manager.save_trial(
            trial=best_trial,
            client=storage,
            db=db,
            collection=collection,
            study_name=manager.name
        )


if __name__ == "__main__":
    for i in range(10):
        asyncio.run(tune(log_folder="logs", config_path="hp_config.yml"))
