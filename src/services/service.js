import axios from 'axios'

/**
 * Variable to avoid rewriting
 */
const ap1 = `${process.env.BACKEND}/api`


export default {

  /**
   * Fetches environments in db
   * 
   * @returns 
   */
  async fetchEnvironments() {
    return await axios.get(api)
  },

  /**
   * Fetches all unique algorithms for an env 
   * 
   * @param {*} env The selected env.
   * @returns All found run-documents with their algorithm
   */
  async fetchAlgs (env) {
    return await axios.get(api + "env_top_trials/?env=" + env)
  },

  /**
   * Fetches the best runs for an algorithm x env combo
   * 
   * @param {*} env The elected environment.
   * @param {*} alg The selected algorithm.
   * @param {*} limit The amount of runs to fetch.
   * @returns at most as many runs as 'limit' states
   */
  async fetchBestRuns (env, alg, limit) {
    return await axios
      .get(api + "alg_top_trials/" + "?env=" + env + "&alg=" + alg + "&limit=" + limit)
  },
  
  /**
   * Fetches a single run
   * 
   * @param {*} run_id The id of the run to fetch.
   * @returns The found run.
   */
  async fetchRun(run_id) {
    return await axios
      .get(api + "runs/" + run_id) 
  },
}
