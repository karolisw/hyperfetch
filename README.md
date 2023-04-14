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

## Quick example
Here is a quick example of how to tune and run PPO in the LunarLander-v2 environment inside your new or existing project:

### 1. Create configuartion  YAML file (minimal example) 

```yaml
# Required
env: LunarLander-v2
alg: ppo

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