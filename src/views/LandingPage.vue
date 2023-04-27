<script>
import Overview from "@/views/Overview.vue";

export default {
  name: "LandingPage",

  async created() {
    await this.$store.dispatch('getEnvironments') 
    this.environmentList = this.$store.getters.GET_ENVS
  },
  data() {
    return {
        environmentList: [], 
        selectedEnvironment: "",
        errorLabel: ""
    };
  },

  methods: {
    async onSelectEnvironment(value) { 
      console.log("the value is: ", value)
      this.selectedEnvironment = value
      // get algs for selected environment and set selected env as current enc
      console.log("selected environment is: ", this.selectedEnvironment)
      await this.$store.dispatch('getAlgorithmsForEnv', {selected_env: this.selectedEnvironment.trim()});
      
      if (this.$store.getters.GET_ALGS.length > 0) {
        this.$router.push({
                  name: 'Overview',
                  component: Overview,
        })
      }
      else {
        this.errorLabel = "Could not find any runs for that environment. Please try selecting another environment"
      }
    },  
  }
}
</script>

<template>  
<div class="landing" title="The landing page for users. Also called Home-page.">
  <section class="home">
    <div class="text container">
      <h2>Fetch Your Hyperparameters</h2>
      <h4>Recreate or find optimal hyperparameters for your Reinforcement Learning project. </h4>
      <h4>Try it out! </h4>
      <label> {{ errorLabel }}</label>
      <div class="text-center">
        <v-menu id="menu"
          open-on-hover rounded="rounded">
          <template v-slot:activator="{ props }">
            <v-btn 
            class="mt-15"
              color="orange-lighten-2"
              v-bind="props"
            >
              Environment
              <v-icon
              end
              icon="mdi-chevron-down"
              size="large"
        ></v-icon>
            </v-btn>
          </template>
          <v-list >
            <v-list-item 
              v-for="(item, index) in environmentList"
              :value="item.env"
              :key="index"
              v-model="selectedEnvironment"
              @click="onSelectEnvironment(item.env)">
              <v-list-item-title>{{ item.env }}</v-list-item-title>
            </v-list-item>
          </v-list>
        </v-menu>
      </div>
    </div>
  </section>
</div>
</template>

<style lang="scss" scoped>
  .home {
    padding-top: 25px;
    background-image: url('../assets/home.jpg');
    background-attachment: fixed;
    background-repeat: round;
    position: relative;
    height: 100vh;

    img {
    object-fit: cover;
    height: 100%;
    width: 100%;
    }

    .text {
      height: 63%;
      display: flex;
      flex-direction: column;
      justify-content: center;
      color: #e5dada;

      .text-center #v-menu v-btn {
        background: blue !important;
      }
    
      h2 {
        font-size: 36px;
        @media (min-width: 550px) {
          font-size: 80px;
        }
      }

      h4 {
        font-size: 20px;
        padding-bottom: 4px;
      }
    }
  }
</style>

