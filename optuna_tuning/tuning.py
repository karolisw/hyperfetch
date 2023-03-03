from codecarbon import track_emissions
from optuna_tuning.manager import Manager
import torch


@track_emissions()  # writes to emissions.csv
def tune(log_folder, config_path):
    manager = Manager(log_folder=log_folder, config_path=config_path)  # todo have i accounted for none-values?

    # Best performing trial is returned
    results = manager.run()

    # Convert trial to model # todo should it be converted to model when being persisted or just when loading?
    # Persist model

if __name__ == "__main__":
    if torch.cuda.is_available():
        cuda_id = torch.cuda.current_device()
        torch.cuda.set_device(cuda_id)

    tune(log_folder="logs", config_path="hp_config.yml")
