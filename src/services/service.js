import axios from 'axios'

const get_envs_endpoint = 'http://localhost:8000/api/' // TODO does this work or should i process differently?
const get_algs_for_env = "http://localhost:8000/api/env_top_trials/?env="
const get_runs_for_alg = "http://localhost:8000/api/alg_top_trials/"
const get_specific_run = "http://localhost:8000/api/runs/"


export default {

    /**
   * Retrieves a list containing all unique environments in db
   *
   * @param adId id for the ad to get
   * @returns {Promise<AxiosResponse<any>>}
   */
  async fetchEnvironments() {
    return await axios.get(get_envs_endpoint)
  },

  // Fetches each algorithm available for an environment (and their best runs
  async fetchAlgs (env) {
    return await axios.get(get_algs_for_env + env)
  },

  // Fetches the best runs for an algorithm (within an environment)
  async fetchBestRuns (env, alg, limit) {
    return await axios
      .get(get_runs_for_alg + "?env=" + env + "&alg=" + alg + "&limit=" + limit)
  },
  
  async fetchRun(run_id) {
    return await axios
      .get(get_specific_run + run_id) 
  },
}
