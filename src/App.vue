<script>
import Navigation from '@/components/Navigation.vue'
  
  export default {
    name: 'App',
    components: {
      Navigation,
    },
    data() {
      return {
        links: ["https://github.com/karolisw/hyperFetch"],
      }
    }
  }
</script>
<template>
  <v-app>
    <div class="app" >
    <Navigation></Navigation>
    <router-view v-slot="{ Component }">
      <transition name="scale-slide" mode="out-in">
        <component :is="Component"></component>
      </transition>
    </router-view>
    </div>
    <v-footer class="bg-blue-grey-darken-4">
      <v-row justify="center" no-gutters>
        <v-btn
          v-for="link in links"
          :key="link"
          color="white"
          variant="text"
          class="mx-2"
          rounded="xl"
        >
          {{ link }}
        </v-btn>
        <v-col class="text-center mt-4" cols="12">
          {{ new Date().getFullYear() }} — <strong>Karoline Sund Wahl @NTNU</strong>
        </v-col>
      </v-row>
    </v-footer>  
  </v-app>
</template>


<style lang="scss">
@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@400;500&display=swap');
* {
  padding: 0;
  margin: 0;
  box-sizing: border-box;
  font-family: "Raleway", sans-serif;
  font-weight: 400;
}

html, body {
  font-family: "Raleway", sans-serif;
  font-style: normal;
}
.app {
  min-height: 100vh;
  position: relative;
  font-family: "Raleway", sans-serif;
  background-color: #8c9eff;
}

.container {
  position: relative;
  padding: 0 20px;
  max-width: 1140px;
  margin: 0 auto;
  line-height: 2;
}

.scale-enter-active,
.scale-leave-active {
  transition: all 0.5s ease-out;
}

.scale-enter-from,
.scale-leave-to {
  opacity: 0;
  transform: scale(0.9);
}

.scale-slide-enter-active,
.scale-slide-leave-active {
  position: absolute;
  transition: all 0.5s ease;
}
.scale-slide-enter-from {
  left: -100%;
}
.scale-slide-enter-to {
  left: 0%;
}
.scale-slide-leave-from {
  transform: scale(1);
}
.scale-slide-leave-to {
  transform: scale(0);
}
</style>
