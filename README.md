# HyperFetch
HyperFetch is a tool to: 
- Make recreation of existing projects easier within the 
  reinforcement learning research community.
- Allow beginners to train and implement their own reinforcement 
  learning models easier due to abstracting away the advanced tuning-step.

The tool is expected to aid in decreasing CO2-emissions related to tuning 
hyperparameters when training RL models. This decrease can happen when
users wish to tune algorithm x environment combinations that have been 
optimially tuned before.

The persistance endpoints opens up to the user through this package.
To access/fetch hyperparameters optimized by other RL-practicioners, 
have a look at the HyperFetch website.

## Links
Repository: [HyperFetch Github](https://github.com/karolisw/hyperFetch)\
Documentation: [HyperFetch Website](https://github.com/karolisw/hyperFetch/tree/frontend)

## Quick example on tuning + posting using HyperFetch
Here is a quick example of how to tune and run PPO in the LunarLander-v2 environment inside your new or existing project:

### 1. Create configuartion  YAML file (minimal example)

```yaml
# Required
alg: ppo
env: LunarLander-v2
project_name: some_project
git_link: github.com/user/some_project

# Some other useful parameters
sampler: tpe
tuner: median
n_trials: 20
log_folder: logs
```

### 2. In a python file

```python
import hyperfetch as hp

# Path to your YAML config file 
path = "../some_folder/config_name.yml"

# Writes each trial's best hyperparameters to log folder
hp.tune(config_path=path)
```

### 3. Enjoy your hyperparameters!

## Quick example on posting hyperparameters not tuned using HyperFetch

### 1. Create configuartion  YAML file 

```yaml
# Required
alg: dqn
env: LunarLander-v2
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

### 2. In a python file

```python
import hyperfetch as hp

# Path to your YAML config file 
path = "../some_folder/config_name.yml"

# Writes each trial's best hyperparameters to log folder
hp.save(config_path=path)
```

### 3. Your hyperparameters are posted. Thank you!
