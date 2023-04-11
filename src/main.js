import { createApp } from 'vue/dist/vue.esm-bundler';
import App from './App.vue';
import router from './router/index.js';
import './style.css';
import store from './store/index.js'    

// Vuetify
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

const vuetify = createVuetify({
  components,
  directives,
})


createApp(App)
//.use(Vuex)
.use(store)
.use(router)
.use(vuetify)
.mount('#app')
