/**
 * Helper-function that maps an algorithm's full name to its abbreviated name
 * 
 * @param {*} fullAlgName The original name.
 * @returns The abbreviated name.
 */
function fromFullToShort(fullAlgName) {
    if (fullAlgName === "Proximal Policy Optimization") return "ppo"
    if (fullAlgName === "Deep Q-Network") return "dqn"
    if (fullAlgName === "Advantage Actor-Critic") return "a2c"
    if (fullAlgName === "Soft Actor-Critic") return "sac"
    if (fullAlgName === "Twin-Delayed DDPG") return "td3"
    
};

/**
 * Helper-function that maps an algorithm's abbreviated name to its full name
 * 
 * @param {*} alg The abbreviated name.
 * @returns The full name.
 */
function fromShortToFull(alg) {

    if (alg === "ppo") return "Proximal Policy Optimization"
    if (alg === "dqn") return "Deep Q-Network"
    if (alg === "a2c") return "Advantage Actor-Critic"
    if (alg === "sac") return "Soft Actor-Critic"
    if (alg === "td3") return "Twin-Delayed DDPG"
    else return "Not implemented yet"
};

export {fromFullToShort, fromShortToFull}; 