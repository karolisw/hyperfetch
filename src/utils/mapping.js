
function fromFullToShort(fullAlgName) {
    if (fullAlgName === "Proximal Policy Optimization") {
        return "ppo"
    }
    else if(fullAlgName === "Deep Q-Network") {
        return "dqn"
    }
    else if(fullAlgName === "Advantage Actor-Critic") {
        return "a2c"
    }
    else if(fullAlgName === "Soft Actor-Critic") {
        return "sac"
    }
    else if(fullAlgName === "Twin-Delayed DDPG") {
        return "td3"
    }
};

function fromShortToFull(alg) {
    
    if (alg === "ppo") return "Proximal Policy Optimization"
    if (alg === "dqn") return "Deep Q-Network"
    if (alg === "a2c") return "Advantage Actor-Critic"
    if (alg === "sac") return "Soft Actor-Critic"
    if (alg === "td3") return "Twin-Delayed DDPG"
    else return "Not implemented yet"
};

export {fromFullToShort, fromShortToFull}; 