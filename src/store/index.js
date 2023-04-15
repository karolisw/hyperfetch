import { createStore } from 'vuex'
import service from "../services/service.js";

export default createStore({
  state: {
    envs:[],
    algs:[],
    runs: [],
    currentEnv: '', 
    currentAlg: '', 
    currentRun: {}, 
    selected_alg: null,
    selected_run: null,
  },
  mutations: {
    ADD_ENV(state, env) {
        state.envs.push(env)
    },
    ADD_ALG(state, alg) {
        state.algs.push(alg)
    },
    ADD_RUN(state, run) {
        state.runs.push(run)
    },
    SET_CURRENT_ENV(state, env) {
        state.currentEnv = env
    },
    SET_CURRENT_ALG(state, alg) {
        state.currentAlg = alg
    },
    SET_CURRENT_RUN(state, run) {
        state.currentRun = run
    },
    SET_ENVS(state, envs) {
        state.envs = envs
    },
    SET_ALGS(state, algs) {
        state.algs = algs
    },
    SET_RUNS(state, runs) {
        state.runs = runs
    },
    SET_SELECTED_ALG(state, alg) {
        state.selected_alg = alg
    },
    SET_SELECTED_RUN(state, run) {
        state.selected_run = run
    }
  },
  getters: {
    GET_ENVS(state) {
        return state.envs
    },
    GET_ALGS(state) {
        return state.algs
    },
    GET_RUNS(state) {
        return state.runs
    },
    GET_CURRENT_ENV(state) {
        return state.currentEnv
    },
    GET_CURRENT_ALG(state) {
        return state.currentAlg
    },
    GET_CURRENT_RUN(state) {
        return state.currentRun
    },
    GET_SELECTED_ALG(state) {
        return state.selected_alg
    },
    GET_SELECTED_RUN(state) {
        return state.selected_run
    }
  },

  actions: {
    async getEnvironments({commit, state}) {
        let response
        try {
            response = await service.fetchEnvironments()
            .then(response => {
                commit('SET_ENVS', response.data)
            })
        } catch (error) {
            console.log('Could not get envs from db with error: ' + error)
        }
    },

    async getAlgorithmsForEnv({commit, state}, selected_env) {
        let response
        try {
            response = await service.fetchAlgs(selected_env.selected_env)
            .then(response => {
                response.data.forEach(element => {
                    element.reward = parseFloat(element.reward).toFixed(3)
                    element.energy_consumed = parseFloat(element.energy_consumed).toFixed(3)
                    element.CO2_emissions = parseFloat(element.CO2_emissions).toFixed(3)
                });
                commit('SET_CURRENT_ENV', selected_env.selected_env)
                commit('SET_ALGS', response.data)
            })
        } catch (error) {
            console.log('Could not get algs for ' + selected_env.selected_env  + ' with error: ' + error)
        }
    },

    /**
     * Fetch single run by id
     * 
     * @param {*} id run ID
     */
       async getRun({commit, state}, param) {
        let id
        try {
            id = param.id
            const existingRun = state.runs.find(run => run.id === id)
            if (existingRun) {
            commit('SET_CURRENT_RUN', existingRun)
            }
            else {
                await service.fetchRun(id)
                .then(response => {
                    response.data.CO2_emissions = parseFloat(response.data.CO2_emissions).toFixed(4)
                    response.data.energy_consumed = parseFloat(response.data.energy_consumed).toFixed(4)
                    response.data.reward = parseFloat(response.data.reward).toFixed(4)
            
                    commit('SET_CURRENT_RUN', response.data)
                })
            }
        } catch (error) {
            console.log('Run with id "' + id + '" not found. \n Error message: ' + error)
        }
        
    },

    /**
     * Fetches the best runs for an algorithm (within an environment)
     * 
     * @param {*} env the env we are searching within
     * @param {*} alg the alg within the env
     * @param {*} limit the amount of runs we wish returned 
     */
    async getRuns({commit, state}, params) {
        let response
        try {
            response = await service.fetchBestRuns(params.env, params.alg, params.limit)
            .then(response => {
                response.data.forEach(element => {
                    element.reward = parseFloat(element.reward).toFixed(3)
                    element.energy_consumed = parseFloat(element.energy_consumed).toFixed(3)
                    element.CO2_emissions = parseFloat(element.CO2_emissions).toFixed(3)
                });
                commit('SET_RUNS', response.data)
            })
        } catch (error) {
            console.log('Could not get runs for '+ params.alg + ' with error: ' + error)
        }
    }
  },
})