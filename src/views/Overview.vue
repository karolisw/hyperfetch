<script>
import Algs from '@/components/Algs.vue';
import Runs from '@/components/Runs.vue';
import Run from '@/components/Run.vue'
import { fromFullToShort } from '@/utils/mapping.js'

export default {
    name: "Overview",
    components: { 
        Algs,
        Runs,
        Run
    },
    data () {
        return {
            displayRuns: false,
            displayRun:false,
            selectedAlg: '',
        }
    },

    methods: {
        async activateRunsOverview(alg) {            
            alg = fromFullToShort(alg)
            this.$store.commit('SET_CURRENT_ALG', alg)

            // Fetch runs for selected alg
            await this.$store.dispatch('getRuns', {
                env: this.$store.getters.GET_CURRENT_ENV, 
                alg: alg, 
                limit: 10
            }) 

            
            // Using prop to tunnel the change down to RunsOverview (child)
            this.selectedAlg = alg

            this.displayRuns = true
            this.displayRun = false
        },

        async activateRunView(run) {
            this.$store.commit('SET_CURRENT_RUN', run)
            this.displayRun = true
        },
        showSelection() {
            this.displayRun = !this.displayRun
        }
    }
}
</script>

<template>  
<v-container class ="parent bg-indigo-accent-1"  fluid align="center">
    <v-row class="btn-row">
        <v-col >
            <v-btn class="returnBtn" v-show="displayRun" @click="showSelection" variant="outlined" transition="fade">
                <v-icon
                center
                icon="mdi-chevron-left"
                size="medium">
                </v-icon>    
                Return
            </v-btn>
        </v-col>
    </v-row>
    <v-row align-self="center" justify-self="center">
        <v-col justify="center">    
            <transition-group name="slide" mode="out-in">
                <Algs v-show="!displayRun" class="algsView" justify="center" @showRuns="activateRunsOverview"></Algs>
                <Runs v-show="!displayRun" class="runsView" justify="center" v-bind:selectedAlg="selectedAlg" v-if="displayRuns" @selectedRun="activateRunView"></Runs>
            </transition-group>
            <transition name="switch" mode="out-in">
                <Run v-if="displayRun" justify="center"></Run>  
            </transition>
        </v-col>
       
    </v-row>

</v-container>

</template>

<style lang="scss" scoped>

.parent {
    padding:0%;
}
.returnBtn {
    margin-right:120vh;
    margin-top: 10vh;
    margin-bottom: -10vh;
}

.runsView {
    margin-left: 5%;
    margin-top: 5%;
    margin-bottom: 5%;
}

.algsView {
    margin-top: 3%;
    margin-left: 5%;
}


.slide-enter-from {
  opacity: 0;
  transform: translateY(160px)
}
.slide-enter-active {
  transition: transform .5s ease,
              opacity .5s ease
}
/* target transform only */
.switch-move {
  transition: transform .3s
}


.switch-enter-from,
.switch-leave-to {
  opacity: 0;
  transform: translateY(200px)
}
.switch-enter-active{
   transition: transform .3s ease,
}


</style>
