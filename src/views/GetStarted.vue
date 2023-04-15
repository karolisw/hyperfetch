<template>

    
    <v-container fluid class="installation">
        <v-row class="box light-bg">
            <v-col cols="12">
                <h1>Page content</h1>
                <hr>
                <br>
                <h3>
                    <ol>
                        <li> <a href="#website-info">Fetching hyperparameters through the website</a></li>
                        <li> <a href="#pip">Tuning and posting your own hyperparameters through the pip-module</a></li>
                        <li> <a href="#post-external">Posting your hyperparameters that are tuned without the use of HyperFetch</a></li>
                        <li> <a href="#hyperfetch-api">The HyperFetch API</a></li>
                    </ol>
                </h3>
            </v-col>
        </v-row>

        <v-row class="box light-bg" id="title"> 
            <v-col cols="12">
                <h1>Fetching hyperparameters</h1> 
                <h3>The following instructions will guide you through fetching hyperparameters through the HyperFetch website.</h3>
            </v-col>  
        </v-row>

        <v-row class="box dark-bg" id="website-info">
            <v-col cols="12">
                <h3>1. You need to know which 
                    <a href="https://www.gymlibrary.dev/">environment</a> you want to train your agent in. 
                </h3>
                <p>If the environment does not yet exist in the 
                    <router-link class="link small" :to="{name: 'Home'}"> dropdown menu</router-link> (home page)
                    , feel free to create hyperparameters for the missing environment using the 
                    <a class="small" href="#pip">pip-module</a>.
                    The environment will show up when it has hyperparameters present in the database. </p>
            </v-col>
        </v-row>
        <v-row class="box dark-bg">
            <v-col cols="12">
                <h3>2. You need to know which 
                    <a href="https://stable-baselines3.readthedocs.io/en/master/guide/algos.html">algorithm</a> you want your agent to train with.
                <br>
                &nbsp; &nbsp; The algorithms currently present are:
                </h3>
                <ul>
                    <li>PPO - Proximal Policy Optimization</li>
                    <li>DQN - Deep Q-Network</li>
                    <li>TD3 - Twin Delayed DDPG</li>
                    <li>SAC - Soft Actor-Critic</li>
                    <li>A2C - Advantage Actor-Critic</li>
                </ul>
            </v-col>
        </v-row>

        <v-row class="box dark-bg">
            <v-col cols="12">
                <h3>3. You are ready to 
                    <router-link class="link" :to="{name: 'Home'}"> fetch hyperparameters!</router-link>
                </h3>

            </v-col>
        </v-row>

        <v-row class="box light-bg" id="pip"> 
            <v-col cols="12">
                <h1>Using HyperFetch in your own project</h1>
                <h3>The following instructions will guide you through the installing and using the HyperFetch pip-module.</h3>
            </v-col>
        </v-row>

        <v-row class="box dark-bg">
            <v-col cols="12">
                <h3>1. Download the pip package into your project</h3>
                <code class="docutils literal notranslate">
                    <span class="pre">pip install hyper-fetch</span>
                </code>
            </v-col>
        </v-row>

        <v-row class="box dark-bg">
            <v-col>
                <h3>2. Make your own 
                    <a href="https://yaml.org/">YAML</a> configuration file</h3>
                <p>A config file could look like this:</p>
                <pre>
                    <code class="language-yaml">
                        # Required config content:
                        alg: ppo 
                        env: LunarLander-v2 
                        project_name: some_project
                        git_link: github.com/user/some_project
                    </code>
                </pre>
                <br><br>
                <p>Or like this when using all parameters (default values):</p>
                <pre>
                    <code class="language-yaml" >
                        # Required config content:
                        alg: ppo
                        env: LunarLander-v2
                        project_name: some_project
                        git_link: github.com/user/some_project

                        # Optional config content:
                        pruner: median
                        policy: MlpPolicy
                        sampler: tpe
                        eval_freq: 10000
                        frame_stack: null
                        log_folder: logs
                        n_envs: 1
                        n_evaluations: 5
                        n_jobs: 1
                        n_min_trials: 1
                        n_startup_trials: 10
                        n_timesteps: 20000
                        n_trials: 10
                        n_warmup_steps: 10
                        name: LunarLander-v2_ppo
                        post_run: true
                        reward_threshold: null
                        seed: 0
                        trial_log_path: logs/trials

                        # Use only when pruner == patient
                        patience: 50
                        min_delta: 0.05

                        # Use only when pruner == percentile
                        percentile: 25.0

                        # Use only when pruner == hyperband 
                        bootstrap_count: 0
                        max_resource: auto
                        min_resource: 1
                        reduction_factor: 3.0

                        # Use only when pruner == threshold
                        lower: 0.0
                        upper: 0.5

                        # Use only when sampler == nsgaii
                        population_size: 50
                        mutation_prob: 0.01
                        crossover_prob: 0.9
                        swapping_prob: 0.5
                    </code>
                </pre>
                <br>
                <p>Tip: Copy either of these into your .yaml file and configure the parameter to your liking. </p>
                <p>As stated in the example, alg and env are the only parameters required for the config file. All other parameters are set to default values unless specified. </p>
                <p>For an in-depth explanation of each parameter, read our 
                    <router-link class="link small" :to="{name: 'ConfigDocs'}"> config docs.</router-link>
                </p>
            </v-col>
        </v-row>

        <v-row class="box dark-bg">
            <v-col cols="12">
                <h3>3. Place the 
                    <router-link class="link" :to="{name: 'ConfigDocs'}"> config file</router-link>
                    inside of your project.  </h3>
            </v-col>
        </v-row>

        <v-row class="box dark-bg">
            <v-col cols="12">
                <h3>4. In a python file, use the <a href="#hyperfetch-api">HyperFetch API</a>.</h3>
                <pre>
                    <code class="language-python">
                        # Import the module
                        import hyper_fetch as hp 

                        # Define your config path. Config can be named anything.
                        config_path = "../ex_folder/config.yml"

                        # Call on the api
                        hp.tune(config_path)

                        # Optimized hyperparameters are saved to your logs folder
                    </code>
                </pre>
            </v-col>
        </v-row>

        <v-row>
            <v-col class="box dark-bg" cols="12">
                <h3>5. Enjoy your new hyperparameters!</h3>
            </v-col>
        </v-row>      
        
        <v-row class="box light-bg" id="post-external">
            <v-col cols="12">
                <h1>Posting your hyperparameters that are not tuned using HyperFetch</h1>
            </v-col>
        </v-row>

        <v-row class="box dark-bg">
            <v-col cols="12">
                <h3>1. Download the pip package into your project</h3>
                <code class="docutils literal notranslate">
                    <span class="pre">pip install hyper-fetch</span>
                </code>
            </v-col>
        </v-row>

        <v-row class="box dark-bg">
            <v-col>
                <h3>2. Make your own 
                    <a href="https://yaml.org/">YAML</a> configuration file.
                    If you already have one, you do not need to make a new one (unless you want to).
                </h3>
                <p>The config file must contain:</p>
                <pre>
                    <code class="language-yaml">
                        # Required config content:
                        alg: dqn 
                        env: LunarLander-v2 
                        project_name: some_project
                        git_link: github.com/user/some_project

                        # The amount and type of hyperparameters will wary 
                        # depending on the chosen algorithm
                        hyperparameters: 
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
                    </code>
                </pre>
                <br><br>
                <p>Or like this when also including all optional parameters:</p>
                <pre>
                    <code class="language-yaml" >
                        # Required config content:
                        alg: ppo
                        env: LunarLander-v2
                        project_name: some_project
                        git_link: github.com/user/some_project
                        hyperparameters: 
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

                        # Optional (if you have the data):
                        CO2_emissions: 0.78 #kgs
                        energy_consumed: 3.27 #kWh
                        cpu_model: 12th Gen Intel(R) Core(TM) i5-12500H
                        gpu_model: NVIDIA GeForce RTX 3070
                        total_time: 0:04:16.842800 # H:M:S:MS
                    </code>
                </pre>
                <br>
                <p>All optional parameters will be given a value of null if not specified.</p>
                <br>
                <strong>Be aware that the reward will not be included when posting external hyperparameters as it cannot be validated.</strong>
                <p>For an in-depth explanation of each parameter, read our 
                    <router-link class="link small" :to="{name: 'ConfigDocs'}"> config docs.</router-link>
                </p>
            </v-col>
        </v-row>

        <v-row class="box dark-bg">
            <v-col cols="12">
                <h3>3. In a python file, use the <a href="#hyperfetch-api">HyperFetch API</a> to save your hyperparameters.</h3>
                <pre>
                    <code class="language-python">
                        # Import the module
                        import hyper_fetch as hp 

                        # Define your config path. Config can be named anything.
                        config_path = "../ex_folder/config.yml"

                        # Call on the api
                        hp.save(config_path)

                        '''
                        Your hyperparameters are saved to the database and viewable on the website
                        The run ID is printed to the console. Filter-search for it after 
                        entering the correct environment on the homepage to see your hyperparameters.
                        '''
                        
                    </code>
                </pre>
            </v-col>
        </v-row>

        <v-row class="box light-bg" id="hyperfetch-api">
            <v-col>
                <h1>The HyperFetch API</h1>
                <h3>Contains entry points to:</h3>
                <ol>
                    <li>Tune <i>and</i> save hyperparameters using HyperFetch</li>
                    <li>Persist hyperparameters not tuned by HyperFetch</li>
                </ol>
            </v-col>
        </v-row>

        <v-row class="box dark-bg">
            <v-col cols="12">
                <h3>The HyperFetch API currently only holds two entry-points (functions)</h3>
                <p>See the
                    <router-link class="link small" :to="{name: 'ConfigDocs'}"> config docs </router-link>
                    for descriptions of which parameters to include. 
                </p>
                <pre>
                    <code class="language-python">
                        # Import the module
                        import hyper_fetch as hp 

                        # Define your config path. Config can be named anything.
                        config_path = "../ex_folder/config.yml"

                        # To tune and persist your hyperparameters 
                        hp.tune(config_path)

                        # To persist existing hyperparameters that are not tuned with HyperFetch
                        hp.save(config_path)
                        
                        '''
                        Your hyperparameters are saved to the database and viewable on the website
                        using either of the two methods.

                        The run ID is printed to the console. Filter-search for it after 
                        entering the correct environment on the homepage to see your hyperparameters.
                        '''
                    </code>
                </pre>
            </v-col>
            <v-col>
                <v-btn  class="scroll-btn"
                v-scroll="onScroll"
                v-show="fab"
                color="indigo darken-3"
                @click="toTop">
                    <v-icon
                    center
                    icon="mdi-chevron-double-up"
                    size="x-large">
                    </v-icon>          
                </v-btn>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>

import Prism from "prismjs";

// Language highlighting in code-blocks
import "prismjs/themes/prism-tomorrow.css"; 
import 'prismjs/components/prism-json'
import 'prismjs/components/prism-bash'
import 'prismjs/components/prism-markdown'
import 'prismjs/components/prism-markup-templating'
import 'prismjs/components/prism-yaml'
import 'prismjs/components/prism-python'
import 'prismjs/plugins/command-line/prism-command-line'

export default {
    name:"GetStarted",
    data() {
        return {
            lineNumbers: "True",
            fab: false
        }
    },

  mounted() {
    Prism.highlightAll(); 
  }, 
  methods: {
    onScroll (e) {
      if (typeof window === 'undefined') return
      const top = window.pageYOffset ||   e.target.scrollTop || 0
      this.fab = top > 20
    },
    toTop () {
        window.scrollTo({
            top: 0,
            left: 0,
            behavior: 'smooth'
        });    
    },
  }
};
</script>

<style lang="scss" scoped>

ul {
  list-style-type: none;
  margin-left: 20px;
  padding: 10px;
  line-height: 30px;
}
    .dark-bg {
            background: #33373d;
            color: #fdf1eb;
    }

    .light-bg {
        margin-top: 80px !important;
        background: #fbdacb;
        color:#202020;
    }

    .box {
        padding: 20px 20px 20px 20px;
        width: 60%;
        margin-left: 100px;
        margin-top: 50px;
        margin-bottom: 50px;
        border-radius: 5px;

        @media(min-width: 900px) {
            border-radius: 5px;
        }
    }

    h1 {
            font-style: normal;
            font-weight: 700;
            font-size: 30px;
            line-height: 30px;
    }
    h2 {
        font-style: normal;
        font-weight: 700;
        font-size: 24px;
        line-height: 26px;
    }
    h3 {
            font-style: normal;
            font-weight: 700;
            font-size: 20px;
            line-height: 26px;
    }

    p {
        margin-top: 16px;
        margin-bottom: 16px;
        font-size: 16px;
        line-height: 24px;
    }

    a {
        text-decoration: none;
        color: #f0885d;
        font-weight: 400;
        font-size: 20px;
        line-height: 20px;
    }

    a:hover {
        color: #c56339;
            font-weight: 700;
    }

    .small {
        font-weight: 400 !important;
        line-height: 20px !important;
        font-size: 16px !important;
        text-decoration: none;
    }
              
    .link {
        font-size: 20px;
    }
    
    .literal {
        padding: 2px 5px;
        background: #433d3d;
        border: 1px solid #e1e4e5;
        color: #1acc4f;
        white-space: normal;
        overflow-x: auto;
        border-radius: 3px;
    }

    .pre {
        padding: 10px;
        font-size: 18px;
    }

    .scroll-btn {
        margin-left:auto;
    }

</style>