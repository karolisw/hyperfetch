export default {
    template: '<img style="width: 25px;" :src="imgStat"/>',
    data() {
      return {
        stat: '',
        imgStat: null,
      };
    },
    methods: {
      refresh(params) {
        this.params = params;
        this.setStat(params);
      },
      setStat(params) {
        this.stat = params.data.param;
        this.imgStat = ".../assets/renderer/run/"
        
        if (this.stat === "CO2 emissions") {
            this.imgStat += "co2.png"
        }
        else if (this.stat === "Energy consumed") {
            this.imgStat += "kwh.png"
        }
        else if (this.stat === "Total time") {
            this.imgStat += "clock.png"
        }
        else if (this.stat === "Reward") {
          this.imgStat += "large_trophy.png"
        }
        else {
          return ""
        }
      },
    },
    created() {
      this.setStat(this.params);
    },
  };