<script>
import AlgsOverview from '../components/AlgsOverview.vue';
import RunsOverview from '../components/RunsOverview.vue';
import { fromFullToShort } from '../utils/mapping.js'
import Run from '../components/Run.vue'

export default {
    name: "Environment",
    components: { 
        AlgsOverview,
        RunsOverview,
        Run
    },
    data () {
        return {
            displayRuns: false,
            displayRun:false,
            selectedAlg: '',
            componentKey: 0,
            componentKey2: 0,
            value: 0,
            interval: 0,
        }
    },

    beforeUnmount () {
    clearInterval(this.interval)
    },
    methods: {
        async activateRunsOverview(alg) {
            this.value = 50
            console.log("current alg: ", alg)
            alg = fromFullToShort(alg)
            this.$store.commit('SET_CURRENT_ALG', alg)

            // Fetch runs for selected alg
            await this.$store.dispatch('getRuns', {
                env: this.$store.getters.GET_CURRENT_ENV, 
                alg: alg, 
                limit: 10
            }) 
            // componentKey mutated as a hack to re-render child component "RunsOverview"
            this.componentKey += 1
            this.componentKey2 += 1
            this.displayRuns = true
            this.displayRun = false
        },

        async activateRunView(run) {
            this.value = 100
            console.log("current alg: ", this.$store.getters.GET_CURRENT_ALG)

            this.$store.commit('SET_CURRENT_RUN', run)
            this.componentKey2 += 1
            this.displayRun = true
        }
    }
}
</script>

<template>  
<v-container class ="parent bg-lime-lighten-5 fluid" fluid >
    <v-row align="start">
        <v-spacer></v-spacer>
        <v-col align-self="center" justify-self="center" flex-grow="0">
            <v-progress-circular align-self="center" justify-self="center"
            :rotate="360"
            :size="80"
            :width="10"
            :model-value="value"
            color="teal">
                {{ value }}
            </v-progress-circular>
        </v-col>
        <v-spacer></v-spacer>

    </v-row>
    <v-row>
        <v-col align-self="start" cols="7"> 
            <transition name="fade" mode="out-in">
                <AlgsOverview class="algsView" :key="componentKey" @showRuns="activateRunsOverview"></AlgsOverview>
            </transition>
            <transition  name="fade" mode="out-in">
                <RunsOverview class="runsView" v-if="displayRuns" :key="componentKey2" @selectedRun="activateRunView"></RunsOverview>
            </transition>
        </v-col>
        <v-col cols="5">
            <Run class="runView" v-if="displayRun" :key="componentKey2" ></Run>
        </v-col>
    </v-row>

</v-container>

</template>

<style scss scoped>

.parent {
    padding:0%;
}

.runsView {
    margin-left: 5%;
    margin-top: 10%;
}

.algsView {
    margin-left: 5%;
}

.runView {
    padding-left: 25px;
}

.fade-enter-to,
.fade-leave.from {
    opacity: 0;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.5s ease-out;
}
</style>
