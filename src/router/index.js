import {createRouter, createWebHistory} from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import Environment from '../views/Environment.vue'
import About from '../views/About.vue'
import UsingPip from '../views/UsingPip.vue'
import ConfigDocs from '../views/ConfigDocs.vue'

/** 
path: the URL path where this route can be found.
name: optional name to use when we link to this route.
component: view to load when this route is called.

We also use createWebHistory to switch from using hash to 
history mode inside the browser, using the HTML5 history API.
*/

const router = createRouter({
  history: createWebHistory(),
  routes: [
      {path: '/', name: 'Home', component: LandingPage},
      {path: '/env', name: 'Environment', component: Environment},
      {path: '/about', name: 'About', component: About},
      {path: '/usingPip', name: 'UsingPip', component: UsingPip},
      {path: '/configDocs', name: 'ConfigDocs', component: ConfigDocs}
  ]
})

export default router;
