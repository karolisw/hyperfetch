<template>
    <v-container fluid class="installation">

        <v-row class="title-box light-bg"> 
            <v-col cols="12">
                <h1>How to use HyperFetch in your own project</h1>
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
                <h3>2. Make your own .yml configuration file</h3>
                <p>A ready-to-use example file could look like this:</p>
                <pre>
                    <code class="language-yaml">
                        # Required config content:
                        alg: ppo 
                        env: LunarLander-v2 
                    </code>
                </pre>
                <p>Or like this (shows default values):</p>
                <pre>
                    <code class="language-yaml" >
                        # Required config content:
                        alg: ppo
                        env: LunarLander-v2

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
                        n_startup_trials: 5
                        n_timesteps: 20000
                        n_trials: 1
                        n_warmup_steps: 0
                        name: LunarLander-v2_ppo
                        post_run: true
                        reward_threshold: -500
                        seed: 1
                        trial_log_path: logs/trials

                        # Use only when pruner == patient
                        patience: 50
                        min_delta: 0.05

                        # Use only when pruner == percentile
                        percentile: 25.0

                        # Use only when pruner == hyperband 
                        bootstrap_count: 0
                        max_resource: auto
                        min_resource: auto
                        reduction_factor: 3.0

                        # Use only when pruner == threshold
                        lower: 0.0
                        upper: 1.0

                        # Use only when sampler == nsgaii
                        population_size: 50
                        mutation_prob: 0.01
                        crossover_prob: 0.9
                        swapping_prob: 0.5
                    </code>
                </pre>
                <p>For the optional values that are not specified, defualt values will be selected for you and written into your config file by the program. </p>
                <p>For an in-depth explanation of each parameter, read our 
                    <router-link class="link" :to="{name: 'ConfigDocs'}"> config docs.</router-link>
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
                <h3>4. In a python file, use the HyperFetch API. </h3>
                <pre>
                    <code class="language-python">
                        # Import the module
                        import hyper_fetch as hp 

                        # Define your config path. Config can be named anything.
                        config_path = "../ex_folder/config.yml"

                        # Call on the api
                        hp.tune(config_path)
                    </code>
                </pre>
            </v-col>
        </v-row>

        <v-row class="box dark-bg">
            <v-col cols="12">
                <h3>5. Run your file for the chosen amount of trials (default: 5, recommended: 10-1000) and wait for the results. 
                    <br><br>
                    Your hyperparameters are printed to the console and saved to your logs folder.</h3>
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
    components: {
    },
    data() {
        return {
            lineNumbers: "True",
        }
    },

  mounted() {
    Prism.highlightAll(); 
  }
};
</script>

<style lang="scss" scoped>


    .title {
        margin-top: 50px;
        margin-left: none !important;
        margin-right: auto !important;
    }
    .dark-bg {
            background: #33373d;
            color: #fdf1eb;
            border-style: solid;
            border-color: rgb(39, 45, 62);

    }

    .light-bg {
        background: #fbdacb;
        color:#202020;
        border-style: solid;
        border-color: rgb(14, 58, 202);
    }

    .title-box {
        padding: 20px 20px 20px 20px;
        width: 70%;
        margin-top: 65px;
        margin-left: 10px;
        margin-bottom: 50px;
        border-radius: 5px;

        @media(min-width: 900px) {
            border-radius: 5px;
        }
    }
    .box {
        padding: 20px 20px 20px 20px;
        width: 60%;
        margin-left: 100px;
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
            margin-bottom:20px;
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
        font-size: 16px;
        line-height: 20px;
    }

    a:hover {
        color: #c56339;
            font-weight: 700;
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

</style>