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

## Content
1.0 [Links](#links)
2.0 [Testing](#testing)
2.1 [Installation backend](#installation-backend)
2.2 [Setup backend](#setup-backend)
2.3 [Setup frontend](#setup-frontend)
2.4 [Installation frontend](#installation-frontend)

3.0 [Pip install (in development)]
3.1 [Website]



## Links
Repository: [HyperFetch Github](https://github.com/karolisw/hyperFetch)\
Documentation: [HyperFetch Website](https://github.com/karolisw/hyperFetch/tree/frontend)

## Testing
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

        Cloning into `HyperFetch`...\
        remote: Counting objects: 10, done.\
        remote: Compressing objects: 100% (8/8), done.\
        remove: Total 10 (delta 1), reused 10 (delta 1)\
        Unpacking objects: 100% (10/10), done.

7. You may now change directory by writing into the terminal:
        
        cd hyperfetch

8. Then, install the dependencies into your virtual environment

         pip install -r requirements.txt


### Set up backend
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

### Set up frontend

1. To serve the website (dev mode), run:

       npm run dev

2. Click the link that appears in the terminal, or access your browser of choice and type in:

       http://localhost:5173/

3. If both the frontend and backend is running now, the websites endpoints should function.
   If they don't, please email me at: karolisw@stud.ntnu.no

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
