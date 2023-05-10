# HyperFetch
#### HyperFetch is a tool consisting of:
- A [website](https://white-rock-097162f03.3.azurestaticapps.net/) for fetching hyperparameters that are tuned by others
- A [pip-module](https://pypi.org/project/hyperfetch/) for tuning and saving hyperparameters yourself 
- NB: Only compatible with Linux distributions due to Box2D-py difficulties of installation on Windows. Might be compatible with MacOS, but not yet tested 

#### The intention of HyperFetch is to:
- Make recreation of existing projects easier within the 
  reinforcement learning research community.
- Allow beginners to train and implement their own reinforcement 
  learning models easier due to abstracting away the advanced tuning-step.

#### The tool is expected to aid in decreasing CO2-emissions related to tuning hyperparameters when training RL models. 
By posting tuned [algorithm x environment] combinations to the website it's expected that:
- Developers/Students can access hyperparameters that have already been optimially tuned instead of having to tune them themselves.
- Researchers can filter by project on the website and access hyperparameters they wish to recreate/replicate for their own research.
- Transparancy related to emissions will become more mainstream within the field.


## Content
* [Links](#links)
* 1.0 [Using the pip module](#using-the-pip-module)
* 2.0 [Examples](#example-1--tuning--posting-using-hyperfetch)


## Links
Repository: [HyperFetch Github](https://github.com/karolisw/hyperFetch)\
How to use config file: [Configuration docs](https://white-rock-097162f03.3.azurestaticapps.net/configDocs)\
Website: [hyperfetch.online](https://white-rock-097162f03.3.azurestaticapps.net/)
API documentation: https://hyperfetch-backend.azurewebsites.net/docs

## Using the pip module
To use the pip model please do the following:

1. Create a virtual environment in your favorite IDE. 

   Install virtualenv if you haven't 
   
           pip install virtualenv
   
   Create a virtual environment
   
           virtualenv [some_name]

   Activate virtualenv this way (Linux/MacOS):
   
            source myvenv/bin/activate
2. Install the pip-module. 

        pip install hyperfetch


         
## Example 1: tuning + posting using HyperFetch
Here is a quick example of how to tune and run PPO in the Pendulum-v1 environment inside your new or existing project:

### Just a reminder:
The pip package must be installed before this can be done.
For details, see [using the pip module](#using-the-pip-module).

### 1. Create configuration file using YAML (minimal example)
If you are unsure of which configuration values to use, see the [config docs](https://white-rock-097162f03.3.azurestaticapps.net/configDocs)

```yaml
# Required (example values)
alg: ppo
env: Pendulum-v1
project_name: some_project
git_link: github.com/user/some_project

# Some other useful parameters
sampler: tpe
tuner: median
n_trials: 20
log_folder: logs
```

### 2. Tune using python file or the command line

```python

from hyperfetch import tuning

# Path to your YAML db_config file 
config_path = "../some_folder/config_name.yml"

# Writes each trial's best hyperparameters to log folder
tuning.tune(config_path)
```

#### Command line:
If in the same directory as the config file and the config file is called "config.yml"

      tune config.yml

If the config file is in another directory and it's called "config.yml"

      tune path/to/config.yml 

#### Enjoy your hyperparameters!

## Example 2: Posting hyperparameters that are not tuned by Hyperfetch

### Just a reminder:
The pip package must be installed before this can be done.
For details, see [using the pip module](#using-the-pip-module).

### 1. Create configuartion  YAML file 
If you are unsure of which configuration values to use, see the [config docs](https://white-rock-097162f03.3.azurestaticapps.net/configDocs)

```yaml
# Required (example values)
alg: dqn
env: Pendulum-v1
project_name: some_project
git_link: github.com/user/some_project
hyperparameters: # These depend on the choice of algorithm
  batch_size: 256
  buffer_size: 50000
  exploration_final_eps: 0.10717928118310233
  exploration_fraction: 0.3318973226098944
  gamma: 0.9
  learning_rate: 0.0002126832542803243
  learning_starts: 10000
  net_arch: medium
  subsample_steps: 4
  target_update_interval: 1000
  train_freq: 8
  
# Not required (but appreciated)
CO2_emissions: 0.78 #kgs
energy_consumed: 3.27 #kWh
cpu_model: 12th Gen Intel(R) Core(TM) i5-12500H
gpu_model: NVIDIA GeForce RTX 3070
total_time: 0:04:16.842800 # H:M:S:MS
```

### 2. Save/post using python file or command line

#### Python file:
```python

from hyperfetch import tuning

# Path to your YAML db_config file 
config_path = "../some_folder/config_name.yml"

# Writes each trial's best hyperparameters to log folder
tuning.save(config_path)
```

#### Command line:
If in the same directory as the config file and the config file is called "config.yml"

      save config.yml