import argparse
from manager import Manager
from codecarbon import EmissionsTracker
from codecarbon import OfflineEmissionsTracker
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from auth_connection import MONGODB_URL, MONGO_DB, MONGO_COLLECTION

client = AsyncIOMotorClient(MONGODB_URL)

# Tracks emissions (writes to emissions.csv)
tracker = EmissionsTracker()

def tune_offline(config_path: str, ISO_code: str) -> None:
    offline_tracker = OfflineEmissionsTracker(country_iso_code=ISO_code
    )
    offline_tracker.start()
    manager = Manager(config_path=config_path)

    # Best performing trial is returned as FrozenTrial
    best_trial = manager.run()

    offline_tracker.stop()

    # Post trial along with the tracking data unless user's config file states not to
    if manager.post_run:
        asyncio.run(manager.save_trial(
            trial=best_trial,
            client=MONGODB_URL,
            db=MONGO_DB,
            collection=MONGO_COLLECTION
        ))

def tune_offline_region(config_path: str, ISO_code: str, region_code:str) -> None:
    offline_tracker = OfflineEmissionsTracker(country_iso_code=ISO_code, region=region_code)
    offline_tracker.start()
    manager = Manager(config_path=config_path)

    # Best performing trial is returned as FrozenTrial
    best_trial = manager.run()

    offline_tracker.stop()

    # Post trial along with the tracking data unless user's config file states not to
    if manager.post_run:
        asyncio.run(manager.save_trial(
            trial=best_trial,
            client=MONGODB_URL,
            db=MONGO_DB,
            collection=MONGO_COLLECTION
        ))

def tune_offline_cloud(config_path: str,cloud_provider:str, cloud_region:str) -> None:
    offline_tracker = OfflineEmissionsTracker(cloud_provider=cloud_provider, cloud_region=cloud_region)
    offline_tracker.start()
    manager = Manager(config_path=config_path)

    # Best performing trial is returned as FrozenTrial
    best_trial = manager.run()

    offline_tracker.stop()

    # Post trial along with the tracking data unless user's config file states not to
    if manager.post_run:
        asyncio.run(manager.save_trial(
            trial=best_trial,
            client=MONGODB_URL,
            db=MONGO_DB,
            collection=MONGO_COLLECTION
        ))


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
    

if __name__ == '__main__':
    #tune_offline("hyperFetch/src/hyperfetch/tuning_parameters.yml","DEU")
    #tune_offline("hyperFetch/src/hyperfetch/tuning_parameters.yml", "DEU")
    #tune_offline("hyperFetch/src/hyperfetch/tuning_parameters.yml", "DEU")

    #tune_offline("hyperFetch/src/hyperfetch/tuning_parameters.yml", "AUS")
    #tune_offline("hyperFetch/src/hyperfetch/tuning_parameters.yml", "AUS")

    #tune_offline("hyperFetch/src/hyperfetch/tuning_parameters.yml", "ESP")
    #tune_offline("hyperFetch/src/hyperfetch/tuning_parameters.yml", "ESP")

    #tune_offline("hyperFetch/src/hyperfetch/tuning_parameters.yml", "IND")
    #tune_offline("hyperFetch/src/hyperfetch/tuning_parameters.yml", "IND")

    #tune_offline("hyperFetch/src/hyperfetch/tuning_parameters.yml", "USA")
    tune_offline("hyperFetch/src/hyperfetch/tuning_parameters.yml", "USA")

    tune_offline("hyperFetch/src/hyperfetch/tuning_parameters.yml", "JPN")
    tune_offline("hyperFetch/src/hyperfetch/tuning_parameters.yml", "JPN")

    tune_offline("hyperFetch/src/hyperfetch/tuning_parameters.yml", "MYS")
    tune_offline("hyperFetch/src/hyperfetch/tuning_parameters.yml", "MYS")

    tune_offline("hyperFetch/src/hyperfetch/tuning_parameters.yml", "TKM")
    tune_offline("hyperFetch/src/hyperfetch/tuning_parameters.yml", "TKM")

    # Tune by region in country
    tune_offline_region("hyperFetch/src/hyperfetch/tuning_parameters.yml", "USA", "KY")
    tune_offline_region("hyperFetch/src/hyperfetch/tuning_parameters.yml", "USA", "kentucky")

    tune_offline_region("hyperFetch/src/hyperfetch/tuning_parameters.yml", "USA", "VT")
    tune_offline_region("hyperFetch/src/hyperfetch/tuning_parameters.yml", "USA", "vermont")


# Tune by cloud provider in order to display the difference inside the same country

# Google cloud platform
    # hong kong (China/Asia)
    tune_offline_cloud(config_path="hyperFetch/src/hyperfetch/tuning_parameters.yml",cloud_provider="gcp",cloud_region="asia-east2")
    # Sydney (Australia/Oseania)
    tune_offline_cloud(config_path="hyperFetch/src/hyperfetch/tuning_parameters.yml",cloud_provider="gcp",cloud_region="australia-southeast1")

    # London (GBR/Europe)
    tune_offline_cloud(config_path="hyperFetch/src/hyperfetch/tuning_parameters.yml",cloud_provider="gcp",cloud_region="europe-west2")

    # Sao Paulo (Brazil/South America)
    tune_offline_cloud(config_path="hyperFetch/src/hyperfetch/tuning_parameters.yml",cloud_provider="gcp",cloud_region="southamerica-east1")

    # Iowa (USA/North America)
    tune_offline_cloud(config_path="hyperFetch/src/hyperfetch/tuning_parameters.yml",cloud_provider="gcp",cloud_region="us-central1")

    # Frankfurt (Germany/Europe) 
    tune_offline_cloud(config_path="hyperFetch/src/hyperfetch/tuning_parameters.yml",cloud_provider="gcp",cloud_region="europe-west3")

# AWS
    # hong kong (China/Asia) 
    tune_offline_cloud(config_path="hyperFetch/src/hyperfetch/tuning_parameters.yml",cloud_provider="aws",cloud_region="ap-east-1")

    # Sydney (Australia/Oseania)
    tune_offline_cloud(config_path="hyperFetch/src/hyperfetch/tuning_parameters.yml",cloud_provider="aws",cloud_region="ap-southeast-2")

    # London (GBR/Europe)
    tune_offline_cloud(config_path="hyperFetch/src/hyperfetch/tuning_parameters.yml",cloud_provider="aws",cloud_region="eu-west-2")
   
    # Sao Paulo (Brazil/South America)
    tune_offline_cloud(config_path="hyperFetch/src/hyperfetch/tuning_parameters.yml",cloud_provider="aws",cloud_region="sa-east-1")

    # Frankfurt (Germany/Europe)
    tune_offline_cloud(config_path="hyperFetch/src/hyperfetch/tuning_parameters.yml",cloud_provider="aws",cloud_region="eu-central-1")



# Azure
    # hong kong (China/Asia)
    tune_offline_cloud(config_path="hyperFetch/src/hyperfetch/tuning_parameters.yml",cloud_provider="azure",cloud_region="eastasia")

    # Sydney (Australia/Oseania)
    tune_offline_cloud(config_path="hyperFetch/src/hyperfetch/tuning_parameters.yml",cloud_provider="azure",cloud_region="australiaeast")

    # Sao Paulo (Brazil/South America)
    tune_offline_cloud(config_path="hyperFetch/src/hyperfetch/tuning_parameters.yml",cloud_provider="azure",cloud_region="brazilsouth")

    # Iowa (USA/North America)
    tune_offline_cloud(config_path="hyperFetch/src/hyperfetch/tuning_parameters.yml",cloud_provider="azure",cloud_region="centralus")