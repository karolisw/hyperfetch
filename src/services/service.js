import {reactive, computed} from 'vue'
import axios from 'axios'


// Variables
let url = 'http://localhost:8000' // evt "mongodb://localhost:"
let port = "8000"


// Endpoint paths (ex: "https://pokeapi.co/api/v2/pokemon?offset=0")
const get_envs_endpoint = 'http://localhost:8000/api/' // TODO does this work or should i process differently?
const get_algs_for_env = "http://localhost:8000/api/env_top_trials/?env="
const get_runs_for_alg = "http://localhost:8000/api/alg_top_trials/"
const get_specific_run = "http://localhost:8000/api/runs/"


export default {

  async fetchEnvironments() {
    return await axios.get(get_envs_endpoint)
  },

  async fetchAlgs (env) {
    return await axios.get(get_algs_for_env + env)
  },

  //http://127.0.0.1:8000/api/alg_top_trials/?env=LunarLander-v2&alg=ppo&limit=10
  async fetchBestRuns (env, alg, limit) {
    return await axios
      .get(get_runs_for_alg + "?env=" + env + "&alg=" + alg + "&limit=" + limit)
  },
  
  async fetchRun(run_id) {
    return await axios
      .get(get_specific_run + run_id) 
  },
  /**
   * Retrieves a list containing all unique environments in db
   *
   * @param adId id for the ad to get
   * @returns {Promise<AxiosResponse<any>>}
   */
  async fetchEnvironments2 () {
    await axios
      .get(get_envs_endpoint)
      .then(response => {
        console.log("response in service: ", response)
        return response;
      });
  },

  // Fetches each algorithm available for an environment (and their best runs)
  async fetchAlgs2 (env) {
    await axios
      .get(get_algs_for_env, 
        {
          params: {
            env
          }})
      .then(response => {
        return response
      });
  },

  // Fetches the best runs for an algorithm (within an environment)
  async fetchBestRuns2 (env, alg, limit) {
    await axios
      .get(get_runs_for_alg,
        {
          params: { // Query params
            env,
            alg,
            limit
        }})
      .then(response => {
        return response
    });
  },

  async fetchRun2(run_id) {
    await axios
      .get(get_specific_run + run_id) 
      .then(response => {
        return response
    });
  }
}
