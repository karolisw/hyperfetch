<script>
import Algs from '../components/Algs.vue';
import Runs from '../components/Runs.vue';
import Run from '../components/Run.vue'
import { fromFullToShort } from '../utils/mapping.js'

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
            value: 0,
        }
    },

    methods: {
        async activateRunsOverview(alg) {
            this.value = 50
            
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
            this.value = 100
            console.log("current alg: ", this.$store.getters.GET_CURRENT_ALG)

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
    <v-row align-self="center" justify-self="center">
        <v-col justify="center">    
            <transition name="fade" mode="in-out" >
                <Algs v-show="!displayRun" class="algsView" justify="center" @showRuns="activateRunsOverview"></Algs>
            </transition>
            <transition name="fade" mode="in-out" >
                <Runs v-show="!displayRun" class="runsView" justify="center" v-bind:selectedAlg="selectedAlg" v-if="displayRuns" @selectedRun="activateRunView"></Runs>
            </transition>
            <v-btn class="returnBtn" v-show="displayRun" @click="showSelection" variant="outlined" transition="fade">
                Return
            </v-btn>
            <transition name="fade" mode="in-out">
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
    margin-top: 5%;
}

.runsView {
    margin-left: 5%;
    margin-top: 5%;
}

.algsView {
    margin-top: 3%;
    margin-left: 5%;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.8s ease-out;
}

.fade-enter-from, 
.fade-leave-to {
  opacity: 0
}

</style>
