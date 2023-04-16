# HyperFetch
#### HyperFetch is a tool consisting of:
- Website for fetching hyperparameters found by others
- Pip-module allowing the user to find hyperparameters 

#### The intention of HyperFetch is to:
- Make recreation of existing projects easier within the 
  reinforcement learning research community.
- Allow beginners to train and implement their own reinforcement 
  learning models easier due to abstracting away the advanced tuning-step.

#### The tool is expected to aid in decreasing CO2-emissions related to tuning hyperparameters when training RL models. 
This is expected to be done by posting tuned algorithm x environment combinations to the websitesuch that:
- Developers/Students can access hyperparameters that have been optimially tuned before instead of having to tune them themselves.
- Researchers can filter by project on the website and access hyperparameters they wish to recreate/replicate for their own research.

The persistance endpoints opens up to the user through this package.
To access/fetch hyperparameters optimized by other RL-practicioners, 
have a look at the HyperFetch website.

## Content
1.0 [Links](#links)\
2.0 [The Website](#getting-the-website-up-and-running)\
2.1 [Installation backend](#installation-backend)\
2.2 [Setup backend](#start-up-backend)\
2.3 [Setup frontend](#start-up-frontend)\
2.4 [Installation frontend](#installation-frontend)

3.0 [Pip install](#installing-pip-package)]\
3.1 [Website]

## Links
Repository: [HyperFetch Github](https://github.com/karolisw/hyperFetch)\
Documentation: [HyperFetch Website](https://github.com/karolisw/hyperFetch/tree/frontend)

## Getting the website up and running
### Installation backend
Make sure you have 
- Pip version 23.0.1 or higher
- Python 3.10
- virtualenv (not venv)
Clone this repository by either:
1. Open git bash 
2. Change the current working directory to the location where you want the cloned directory.
3. Paste this snip:

        git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY

4. Install virtualenv if you haven't 

        pip install virtualenv

5. Create a virtual environment

        virtualenv [some_name]

    Activate virtualenv this way if using windows:

       # In cmd.exe
       venv\Scripts\activate.bat
       # In PowerShell
       venv\Scripts\Activate.ps1

    Activate virtualenv this way if using Linux/MacOS:

        $ source myvenv/bin/activate

6. Press Enter to create your local clone.

        Cloning into 'hyperFetch'...
        remote: Enumerating objects: 466, done.
        remote: Counting objects: 100% (466/466), done.
        remote: Compressing objects: 100% (238/238), done.
        remote: Total 466 (delta 221), reused 438 (delta 200), pack-reused 0
        Receiving objects: 100% (466/466), 4.17 MiB | 10.29 MiB/s, done.
        Resolving deltas: 100% (221/221), done.

7. You may now change directory by writing into the terminal:
        
        cd hyperfetch

8. Then, install the dependencies into your virtual environment

         pip install -r requirements.txt


### Start up backend
After cloning and installing, you can finally start up the server!

          uvicorn main:app --reload   
        

### Installation frontend
The frontend-branch is inside of the same project. However, 
because the frontend-branch (frontend) and backend-branch (master)
must run at the same time to serve the website, 
the project must be cloned twice into two different local respositories. 

1. Follow stages 3-6 in [installation backend](#installation-backend) 
   This includes:
   - Move into another working directory
   - Clone the project
   - Create a new virtualenv
   - Activate the virtualenv

3. The frontend-branch does not exist locally and must be fetched remotely. 
   In the terminal, type: 

       git switch frontend

4. Enter the correct folder
       
       cd src
5. Install dependencies. This will creat a node_modules folder in your local repository.

       npm install

### Start up frontend

1. To serve the website (dev mode), run:

       npm run dev

2. Click the link that appears in the terminal, or access your browser of choice and type in:

       http://localhost:5173/

3. Good luck!

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

from src import hyperfetch as hp

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

from src import hyperfetch as hp

# Path to your YAML config file 
path = "../some_folder/config_name.yml"

# Writes each trial's best hyperparameters to log folder
hp.save(config_path=path)
```

### 3. Your hyperparameters are posted. Thank you!

## Installing pip package
