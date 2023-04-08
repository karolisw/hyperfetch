<template>
    <v-container>

        <v-row class="title"> 
            <v-col cols="12">
                <h1>How to use HyperFetch in your own project</h1>
            </v-col>
        </v-row>

        <v-row>
            <v-col cols="12">
                <h3>1. Download the pip package into your project</h3>
                <code class="language-bash">
                    pip install hyper-fetch
                </code>
                
            </v-col>
        </v-row>

        <v-row>
            <v-col>
                <h3>2. Make your own .yml configuration file</h3>
            </v-col>
        </v-row>

        <v-row justify="center">
            <v-col cols="6" >
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

        <v-row>
            <v-col cols="12">
                <h3>3. Place the config file inside of your project.  </h3>
            </v-col>
        </v-row>

        <v-row>
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

        <v-row>
            <v-col cols="12">
                <h3>5. Your hyperparameters will print to the console.</h3>
            </v-col>
        </v-row>
        
    </v-container>
</template>

<script>
/**
 *   <PrismTemplate lineNumbers="lineNumbers">
                </PrismTemplate>
 */
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

//import PrismTemplate from "../components/PrismTemplate.vue";
export default {
    name:"UsingPip",
    components: {
        //PrismTemplate,
    },
    data() {
        return {
            lineNumbers: "True",
        }
    },

  // mounted
  mounted() {
    Prism.highlightAll(); // highlight your code on mount
  }
};
</script>