export default {
    template: '<img style="width: 25px;" :src="imgForAlg" />',
    data() {
      return {
        alg: '',
        imgForAlg: null,
      };
    },
    methods: {
      refresh(params) {
        this.params = params;
        this.setAlg(params);
      },
      setAlg(params) {
        this.alg = params.data.full;
        this.imgForAlg = "/assets/renderer/alg/"
        
        if (this.alg === "Proximal Policy Optimization") {
            this.imgForAlg += "ppo.png"
        }
        else if(this.alg === "Deep Q-Network") {
            this.imgForAlg += "dqn.png"
        }
        else if(this.alg === "Advantage Actor-Critic") {
            this.imgForAlg += "a2c.png"
        }
        else if(this.alg === "Soft Actor-Critic") {
            this.imgForAlg += "sac.png"
        }
        else if(this.alg === "Twin-Delayed DDPG") {
            this.imgForAlg += "td3.png"
        }
        else {
            this.imgForAlg += "none.png"
        }
      },
    },
    created() {
      this.setAlg(this.params);
    },
  };