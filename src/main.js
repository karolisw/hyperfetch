import { createApp } from 'vue/dist/vue.esm-bundler';
import App from './App.vue';
import router from './router/index.js';
import store from './store/index.js'    

// Vuetify modules
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css' 

const vuetify = createVuetify({
  components,
  directives,
  iconfont: 'mdi'
})


createApp(App)
.use(store)
.use(router)
.use(vuetify)
.mount('#app')
