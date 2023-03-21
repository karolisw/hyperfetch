from optuna_tuning.manager import Manager
from codecarbon import EmissionsTracker
import asyncio
from utils import common

storage = utils.get_yaml_val("../config/db_config.yml", "storage")
db = utils.get_yaml_val("../config/db_config.yml", "db")
collection = utils.get_yaml_val("../config/db_config.yml", "collection")

# Tracks electricity usage in kWh (writes to emissions.csv)
tracker = EmissionsTracker()


async def tune(log_folder, config_path):
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
            trial=best_trial, client=storage, db=db,
            collection=collection, study_name=manager.name
        )


if __name__ == "__main__":
    asyncio.run(tune(log_folder="logs", config_path="hp_config.yml"))
