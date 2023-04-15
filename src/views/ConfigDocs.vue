<template>
    <div class="config-container">
        <section id="parameters">
                <section class="text box light-bg">
                    <h1>
                        Parameters for configuration file
                    </h1>
                    <br>
                    <ol>
                        <li><a href="#main-parameters">Parameters for tuning and persisting using HyperFetch</a></li>
                        <li><a href="#pruners">Parameters usable with specific pruner </a></li>
                        <li><a href="#samplers">Parameters usable with specific sampler</a></li>
                        <li><a href="#external-parameters">Parameters for persisting hyperparameters not produced using HyperFetch</a></li>
                    </ol>
                    <br>
                    <p>
                        The intention of these parameters is to help users provide additional details for HyperFetch when tuning their RL project. 
                        This will aid in optimizing the search for hyperparameters.
                    </p>
                </section>
            <section id="main-parameters">
                <div class="text box has-table dark-bg">
                    <h3>Parameters for tuning and persisting using HyperFetch.</h3>
                    <p>These parameters can be used with <i>any</i> sampler and pruner.</p>
                </div>
                <div class="ag-table">
                    <ag-grid-vue 
                    @grid-ready="onGridReady"
                    style="width: 120vh;"
                    class="ag-theme-alpine-dark"
                    :columnDefs="columnDefs"
                    :defaultColDef="defaultColDef"
                    :rowData="rowData"
                    :domLayout="domLayout">
                    </ag-grid-vue>
                </div>
            </section>

            <section class="pruners" id="pruners"> 
                <div class="text box light-bg">
                    <h2> Pruners</h2>
                    <p>Optuna is the framework that tunes the hyperparameters inside of the application. Whilst HyperFetch with its single-function API makes the optimization seeminly more of a black-box; 
                        the user is granted the ability to configure their own pruner and sampler, alongside all the other configurable parameters. 
                        The pruner decides which trials perform well enough to keep training, and which trials to end. 
                    </p>
                </div>
                <section class="text box dark-bg" id="sh-pruner">
                    <h3>SuccessiveHalvingPruner</h3>
                    <p> The SuccessiveHalvingPruner uses an Asynchronous Successive Halving Algorithm. Successive Halving is a bandit-based algorithm
                        that identifies the best one among multiple configurations. This pruner implements an asynchronous 
                        version of Successive Halving.  
                        The SuccessiveHalving pruner is derived of the 
                        <a class="small" href="https://arxiv.org/abs/1810.05934">Massively Parallel </a> hyperparameter tuning paper.
                    </p>
                </section>
                <section class="text box dark-bg">
                    <h3>Median Pruner</h3>
                    <p>The median pruner uses the median stopping rule. 
                        <br>
                        The median stopping rule says that the Trial
                        should be pruned if the best intermediate result is worse than the median of intermediate results of previous trials at the same step.
                        This pruner is the default pruner of the application.
                    </p>
                </section>
                <section>
                    <div class="text box has-table dark-bg">
                        <h3>Patient Pruner</h3>
                        <p>The patient pruner is a pruner that wraps another pruner with tolerance. When selecting this pruner, the tolerance is wrapped around a Median Pruner.
                        Patient Pruner is an experimental feature, meaning it will be removed from future versions of HyperFetch if Optuna provides a good reasoning for its demise.
                        </p>
                    </div>
                    <div class="ag-table">
                        <ag-grid-vue 
                        @grid-ready="onPatientReady"
                        style="width: 120vh;"
                        class="ag-theme-alpine-dark"
                        :columnDefs="columnDefs"
                        :defaultColDef="defaultColDef"
                        :rowData="rowPatience"
                        :domLayout="domLayout">
                        </ag-grid-vue>
                    </div>
                </section>
                <section>
                    <div class="text box has-table dark-bg">
                        <h3>Percentile Pruner</h3>
                        <p>The percentile pruner is a pruner that keeps the specified percentile of the trials. 
                        Percentile pruner prunes if the best intermediate value is in the bottom percentile among trials at the same step.
                        </p>
                    </div>
                    <div class="ag-table">
                        <ag-grid-vue 
                        @grid-ready="onPercentileReady"
                        style="width: 120vh;"
                        class="ag-theme-alpine-dark"
                        :columnDefs="columnDefs"
                        :defaultColDef="defaultColDef"
                        :rowData="rowPercentile"
                        :domLayout="domLayout">
                        </ag-grid-vue>
                    </div>
                </section>
                <section>
                    <div class="text box has-table dark-bg">
                        <h3>Hyperband Pruner</h3>
                        <p>The hyperband pruner is derived of the 
                            <a class="small" href="https://www.jmlr.org/papers/volume18/16-558/16-558.pdf">Hyperband paper</a>.
                            <br>
                            If you use hyperband pruner with 
                            <a class="small" href="#tpe-sampler">TPESampler</a> , it's recommended to consider setting larger
                            <a class="small" href="#main-parameters">n_trials</a> to make full use of the characteristics of 
                            <a class="small" href="#tpe-sampler">TPESampler</a> .This is because
                            <a class="small" href="#tpe-sampler">TPESampler</a> uses a number of (default: 10)
                            <a class="small" href="#main-parameters">Trials</a> for its startup. As Hyperband runs multiple 
                            <a class="small" href="#sh-pruner">SuccessiveHalvingPruner</a> and collects trials based on the current 
                            <a class="small" href="#main-parameters">Trials</a> bracket ID, each bracket needs to observe more than 10 
                            <a class="small" href="#main-parameters">Trials</a> for
                            <a class="small" href="#tpe-sampler">TPESampler</a> to adapt its search space. 
                            <br>
                            Selecting the number of pruners for this pruner to have is done by choosing values for 
                            <a class="small" href="#main-parameters">min_resource</a>, 
                            <a class="small" href="#main-parameters">max_resource</a> and 
                            <a class="small" href="#main-parameters">reduction_factor</a>
                            (see Section 3.6 of the <a class="small" href="https://www.jmlr.org/papers/volume18/16-558/16-558.pdf">original paper</a> for details).
                            <br><br>
                            <strong>Example</strong>: If HyperbandPruner has 4 pruners in it, at least 4 x 10 trials are consumed for startup.
                        </p>
                        </div>
                        <div class="ag-table">
                            <ag-grid-vue 
                            @grid-ready="onHyperbandReady"
                            style="width: 120vh;"
                            class="ag-theme-alpine-dark"
                            :columnDefs="columnDefs"
                            :defaultColDef="defaultColDef"
                            :rowData="rowHyperband"
                            :domLayout="domLayout">
                            </ag-grid-vue>
                        </div>
                    </section>
                    <section>
                        <div class="text box has-table dark-bg">
                            <h3>Threshold Pruner</h3>
                            <p>The threshold pruner is a pruner to detect outlying metrics of the trials. A trial is pruned if a metric exceeds upper threshold,
                                falls behind lower threshold or reaches
                                <code class="docutils literal notranslate">
                                    <span class="pre">nan</span>
                                </code>
                            </p>
                        </div>
                        <div class="ag-table">
                            <ag-grid-vue 
                            @grid-ready="onThresholdReady"
                            style="width: 120vh;"
                            class="ag-theme-alpine-dark"
                            :columnDefs="columnDefs"
                            :defaultColDef="defaultColDef"
                            :rowData="rowThreshold"
                            :domLayout="domLayout">
                            </ag-grid-vue>
                        </div>
                </section>

            </section>
            <section class="samplers" id="samplers">
                <div class="text box light-bg">
                    <h2> Samplers</h2>
                    <p>Optuna combines two types of sampling strategies, which are called relative sampling and independent sampling.
                        Read more about them 
                        <a class="small" href="https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler">here</a>.
                        The application utilizes all Samplers except the GridSampler due to the nature of the RL problem (too many combinations).
                        For a better understanding of when to use which sampler, see the 
                        <a class="small" href="https://optuna.readthedocs.io/en/stable/reference/samplers/index.html">comparison chart</a>.
                    </p>
                </div>
                <section>
                    <div class="text has-table box dark-bg">
                        <h3>NSGAIISampler</h3>
                        <p>The NSGAII sampler is a multi-objective sampler that uses the 
                            <a class="small" href="https://ieeexplore.ieee.org/document/996017">NSGA-II algorithm</a>.
                            NSGA-II stands for “Nondominated Sorting Genetic Algorithm II”. NSGA-II is a well known, fast and elitist multi-objective genetic algorithm.
                        </p>
                    </div>
                    <div class="ag-table">
                        <ag-grid-vue 
                        @grid-ready="onNsgaiiReady"
                        style="width: 120vh;"
                        class="ag-theme-alpine-dark"
                        :columnDefs="columnDefs"
                        :defaultColDef="defaultColDef"
                        :rowData="rowNsgaii"
                        :domLayout="domLayout">
                        </ag-grid-vue>
                    </div>
                </section>
                <section class="text box dark-bg">
                    <h3>RandomSampler</h3>
                    <p>The random sampler uses random sampling. This sampler is based on independent sampling. 
                        See also 
                        <a class="small" href="https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler">BaseSampler</a>
                        for more details of 'independent sampling'.
                    </p>
                </section>
                <section class="text box dark-bg">
                    <h3>CmaEsSampler</h3>
                    <p>The CmaEs sampler is a sampler that uses 
                        <a class="small" href="https://github.com/CyberAgentAILab/cmaes">cmaes</a>. CMAES stands for "(Lightweight) Covariance Matrix Adaptation Evolution Strategy".
                    </p>
                </section>
                <section class="text box dark-bg" id="tpe-sampler">
                    <h3>TPESampler</h3>
                    <p>The TPE sampler is a multi-objective sampler that uses the TPE (Tree-structured Parzen Estimator) algorithm. 
                        This sampler is based on independent sampling.  See also 
                        <a class="small" href="https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.BaseSampler.html#optuna.samplers.BaseSampler">BaseSampler</a>
                        for more details of 'independent sampling'.
                        <br> 
                        On each trial, for each parameter, TPE fits one Gaussian Mixture Model (GMM) &nbsp;
                        <strong>l(x)</strong> &nbsp; to the set of parameter values associated with the best objective values, and another GMM &nbsp;
                        <strong>g(x)</strong> &nbsp; to the remaining parameter values. It chooses the parameter value &nbsp;
                        <strong>x</strong> &nbsp; that maximizes the ratio &nbsp;
                        <strong>l(x)/g(x)</strong>.
                    </p>
                </section>
                <section class="text box dark-bg">
                    <div>
                        <h3>SkoptSampler</h3>
                        <p>The skopt sampler uses Scikit-Optimize as the backend. This sampler optimizes its hyperparameters by optimizing a simple quadratic equation.
                            Read more 
                            <a class="small" href="https://optuna.readthedocs.io/en/stable/reference/generated/optuna.integration.SkoptSampler.html#optuna.integration.SkoptSampler">here</a>.
                            No parameters are available for this sampler and it will run as default. 
                        </p>
                    </div>
                </section>
            </section>

            <section id="external-parameters">
                <div class="text box light-bg">
                    <h2>Parameters for persisting hyperparameters not produced using HyperFetch</h2>
                    <p>This section is relevant for those who wish to post their hyperparameters to HyperFetch,
                        without having tuned said hyperparameters using HyperFetch. 
                    </p>
                </div>
                <div class="ag-table">
                    <ag-grid-vue 
                    @grid-ready="onExternalReady"
                    style="width: 120vh;"
                    class="ag-theme-alpine-dark"
                    :columnDefs="columnDefs"
                    :defaultColDef="defaultColDef"
                    :rowData="rowExternal"
                    :domLayout="domLayout">
                    </ag-grid-vue>
                </div>
                <v-btn class="up-btn"
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
            </section>
        </section>
    </div>
</template>

<script>
import { AgGridVue } from "ag-grid-vue3";
import "ag-grid-community/styles//ag-grid.css";
import "ag-grid-community/styles//ag-theme-alpine.css";

export default {
  name: "ConfigDocs",
  components: {
    AgGridVue,
  },

    created() {

        // Define grid headers
        this.columnDefs= [
        { headerName: "Parameter", field: "parameter", minWidth: 200, maxWidth: 200, wrapText:true, autoHeight:true},
        { headerName: "Description", field: "description", wrapText:true, autoHeight:true},  
        ]

        // Make rows adjust height according to amount of rows (automatically)
        this.domLayout = "autoHeight"
        this.defaultColDef = {
            editable: false,
            sortable: true,
            flex: 1,
            minWidth: 100,
            filter: true,
            resizable: true,
        }

        // Parameters and values    
        this.data = {
            "alg (str)": "Required. Reinforcement learning algorithms build a model of the environment by sampling the states, taking actions, and observing the rewards. Also called agent. ",
            "env (str)": "Required. The environment is where the agent learns and decides what actions to perform. In HyperFetch, environments from Stable-Baselines3 are used.",
            "project_name (str)": "Required. Is the name of the project that the hyperparameters belong to. If the hyperparameters are not related to a project, simply assign an empty string to this parameter.",
            "git_link (str)": "Required. Is the link to the Git repository connected to the project your hyperparameters belong to. If the project is not uploaded to Git, simply assign an empty string to this parameter.",
            "sampler (str)": "A sampler has the responsibility to determine the parameter values to be evaluated in a trial. Defaults to TPE.",
            "pruner (str)": "Returns a boolean value representing whether the trial should be pruned. Default pruner is the MedianPruner.",
            "frame_stack (int)": "The number of frames to stack when using VecFrameStack (stacking wrapper for vectorized environment). Designed for image observations, meaning environments where the state is RGB-arrays.",
            "log_folder (str)": "Should contain the folder that the user wishes to log trials to. Defaults to 'logs'.",
            "n_envs (int)": "The number of environments.",
            "n_evaluations (int)": "Evaluations for TrialEvalCallback.",
            "n_jobs (int)": "The number of parallel jobs. If this argument is set to ``-1``, the number is set to CPU count. If ``n_jobs`` is greater than one or if another signal than SIGINT is used, the interrupted trial state won't be properly updated",
            "n_min_trials (int)": "Minimum number of reported trial results at a step to judge whether to prune. If the number of reported intermediate values from all trials at the current step is less than ``n_min_trials``, the trial will not be pruned. This can be used to ensure that a minimum number of trials are run to completion without being pruned.",
            "n_startup_trials (int)": "Pruning is disabled until the given number of trials finish in the same study.",
            "n_timesteps (int)": "Timesteps for the RL model.",
            "n_trials (int)": "The number of trials for each process. None represents no limit in terms of the number of trials. The study continues to create trials until the number of trials reaches n_trials, or until receiving a SIGTERM -or SIGINT signal.",
            "n_warmup_steps (int)": "Pruning is disabled if the step is less than the given number of warmup steps.",
            "policy (str)": "The decision-making function (control strategy) of the agent, which represents a mapping from situations to actions.",
            "post_run (bool)": "Whether or not to post the best performing hyperparameters of the study to HyperFetch.",
            "reward_threshold (float)": "A threshold for early stopping. The program will stop (even if all trials are not completed) when this reward threshold is reached.",
            "seed (int)": "Seed for the samplers Random number generator. Defaults to 0.",
            "trial_log_path (str)": "The path to where the results for each trial will be saved. Defaults to 'logs/trials'",
        }

        this.nsgaii = {
            "population_size": "Number of individuals (trials) in a generation. Defaults to 50.",
            "swapping_prob": "Probability of swapping each parameter of the parents during crossover. Defaults to 0.5.",
            "crossover_prob": "Probability that a crossover (parameters swapping between parents) will occur when creating a new individual. Defaults to 0.9",
            "mutation_prob": " Probability of mutating each parameter when creating a new individual. If None is specified, the value 1.0 / len(parent_trial.params) is used where parent_trial is the parent trial of the target individual. Defaults to 0.01.",
        },
        this.threshold = {
            "lower (float)": "A minimum value which determines whether pruner prunes or not. If an intermediate value is smaller than lower, it prunes.",
            "upper (float)": "A maximum value which determines whether pruner prunes or not. If an intermediate value is larger than upper, it prunes.",
        },
        this.hyperband = {
            "bootstrap_count (int)" : "Parameter specifying the number of trials required in a rung before any trial can be promoted into the next rung. A rung is the number of steps a trial takes each round. Incompatible with max_resource == 'auto'.",
            "reduction_factor (int)": "A parameter for specifying reduction factor of promotable trials. ",
            "max_resource (str|int)": "A parameter for specifying the maximum resource allocated to a trial. This value represents and should match the maximum iteration steps (e.g., the number of epochs for neural networks). When this argument is “auto”, the maximum resource is estimated according to the completed trials. The default value of this argument is “auto”.",
            "min_resource (int)": " A parameter for specifying the minimum resource allocated to a trial. A smaller value will give a result faster, but a larger value will give a better guarantee of successful judging between configurations. ",
        },
        this.percentile = {
            "percentile (float)": "A percentile representing the amount of pruners to keep. Percentile which must be between 0 and 100 inclusive (e.g., When given 25.0, top of 25th percentile trials are kept).",
        }
        this.patience = {
            "min_delta (float)": "Tolerance value to check whether or not the objective improves. This value should be non-negative.",
            "patience (int)": "Pruning is disabled until the objective doesn't improve for patience consecutive steps.",
        }
        this.external = {
            "alg (str)": "Required. Reinforcement learning algorithms build a model of the environment by sampling the states, taking actions, and observing the rewards. Also called agent. ",
            "env (str)": "Required. The environment is where the agent learns and decides what actions to perform. In HyperFetch, environments from Stable-Baselines3 are used.",
            "project_name (str)": "Required. Is the name of the project that the hyperparameters belong to. If the hyperparameters are not related to a project, simply assign an empty string to this parameter.",
            "git_link (str)": "Required. Is the link to the Git repository connected to the project your hyperparameters belong to. If the project is not uploaded to Git, simply assign an empty string to this parameter.",
            "CO2_emissions": "The CO2 emissions (kgs) produced by tuning your hyperparameters. Use only when posting hyperparameters not tuned with HyperFetch.",
            "energy_consumed": "The kWh spent tuning your hyperparameters.Use only when posting hyperparameters not tuned with HyperFetch.",
            "cpu_model": "The CPU model used to tune your hyperparameters. If you have used a Cloud hosting platform or something of the sort, it's enough to name it. Use only when posting hyperparameters not tuned with HyperFetch.",
            "gpu_model": "The GPU model used to tune your hyperparameters. If you have used a Cloud hosting platform or something of the sort, it's enough to name it. Use only when posting hyperparameters not tuned with HyperFetch.",
            "total_time": "The total time spent tuning your hyperparameters. Format: Hours:Minutes:Seconds:Miliseconds. Use only when posting hyperparameters not tuned with HyperFetch.",
        }
    },

    data() {
        return {
            defaultColDef: null,
            gridApi: null, 
            columnApi: null,
            domLayout: null,
            columnDefs: [],
            data: [],
            nsgaii: [],
            threshold: [],
            hyperband: [],
            percentile: [],
            patience: [],
            external: [],
            rowData: [],
            rowNsgaii: [],
            rowThreshold: [],
            rowHyperband: [],
            rowPercentile: [],
            rowPatience: [],
            rowExternal: [],
            fab: false
        }
    },
    methods: {
        onGridReady(params) {
        this.gridApi = params.api;
        this.gridColumnApi = params.columnApi;

        this.gridApi.sizeColumnsToFit(params)

        const updateData = (data) => params.api.setRowData(data);

        // Format data
        for (const [key, value] of Object.entries(this.data)) {
            this.rowData.push({parameter: key, description: value})
        }
       
        updateData(this.rowData)
        },

        onPatientReady(params) {
        this.gridApi = params.api;
        this.gridColumnApi = params.columnApi;

        const updateData = (data) => params.api.setRowData(data);

        // Format data
        for (const [key, value] of Object.entries(this.patience)) {
            this.rowPatience.push({parameter: key, description: value})
        }
       
        updateData(this.rowPatience)
        },

        onPercentileReady(params) {
        this.gridApi = params.api;
        this.gridColumnApi = params.columnApi;

        const updateData = (data) => params.api.setRowData(data);

        // Format data
        for (const [key, value] of Object.entries(this.percentile)) {
            this.rowPercentile.push({parameter: key, description: value})
        }
       
        updateData(this.rowPercentile)
        },

        onThresholdReady(params) {
        this.gridApi = params.api;
        this.gridColumnApi = params.columnApi;

        const updateData = (data) => params.api.setRowData(data);

        // Format data
        for (const [key, value] of Object.entries(this.threshold)) {
            this.rowThreshold.push({parameter: key, description: value})
        }
       
        updateData(this.rowThreshold)
        },

        onNsgaiiReady(params) {
        this.gridApi = params.api;
        this.gridColumnApi = params.columnApi;

        const updateData = (data) => params.api.setRowData(data);

        // Format data
        for (const [key, value] of Object.entries(this.nsgaii)) {
            this.rowNsgaii.push({parameter: key, description: value})
        }
       
        updateData(this.rowNsgaii)
        },

        onHyperbandReady(params) {
        this.gridApi = params.api;
        this.gridColumnApi = params.columnApi;

        const updateData = (data) => params.api.setRowData(data);

        // Format data
        for (const [key, value] of Object.entries(this.hyperband)) {
            this.rowHyperband.push({parameter: key, description: value})
        }
        updateData(this.rowHyperband)
        },

        onExternalReady(params) {
        this.gridApi = params.api;
        this.gridColumnApi = params.columnApi;

        const updateData = (data) => params.api.setRowData(data);

        // Format data
        for (const [key, value] of Object.entries(this.external)) {
            this.rowExternal.push({parameter: key, description: value})
        }
        updateData(this.rowExternal)
        },

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
}
</script>

<style lang="scss" scoped>
.ag-theme-alpine-dark {
    --ag-borders: 5px;
    --ag-borders-critical: solid 1px;
    --ag-critical-border-color:var(--ag-foreground-color);
    --ag-background-color:  #33373d;
    --ag-foreground-color: #fdf1eb;
    --ag-header-background-color: rgb(43, 102, 43);
}

.config-container {
    display: flex;
    justify-content: center;
    margin-left: 100px;

    .up-btn {
        margin-left: 130vh;
    }
    .ag-table {
        margin-top: 5px;
    }
    .text {
        h1 {
            font-weight: 700;
            font-size: 30px;
            line-height: 30px;
        }
        h2 {
            font-weight: 700;
            font-size: 24px;
            line-height: 26px;
        }
        h3 {
            font-weight: 700;
            font-size: 20px;
            line-height: 26px;
        }

        p {
            font-size: 16px;
            line-height: 28px;
        }

        a {
            text-decoration: none;
            color: #f0885d;
            font-weight: 700;
            font-size: 20px;
            line-height: 30px;
        }

        a:hover {
            color: #c56339;
            font-weight: 700;
        }
        
        code {
            padding: 1px 3px;
            margin-left: 2px;
            margin-right: 2px;
            background: #fff;
            border: 1px solid #e1e4e5;
            color: #e74c3c;
            overflow-x: auto;
            .literal {
                color: #e74c3c;
                white-space: normal;
            }
            .pre {
                font-weight: bold;
            }
        }
    }

    .small {
        font-weight: 400 !important;
        line-height: 20px !important;
        font-size: 16px !important;
        text-decoration: none;
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
        padding: 30px 30px 30px 30px;
        width: 73%;
        margin-top: 50px;
        margin-bottom: 50px;
        border-radius: 5px;

        @media(min-width: 900px) {
            border-radius: 5px;
        }
    }
    .has-table {
            margin-bottom: 0px !important;
    }
    #external-parameters {
        margin-bottom:35vh;
    }
}
</style>