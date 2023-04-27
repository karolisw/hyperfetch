import {createRouter, createWebHistory} from 'vue-router'
import LandingPage from '@/views/LandingPage.vue'
import Overview from '@/views/Overview.vue'
import About from '@/views/About.vue'
import GetStarted from '@/views/GetStarted.vue'
import ConfigDocs from '@/views/ConfigDocs.vue'

/** 
path: the URL path where this route can be found.
name: optional name to use when we link to this route.
component: view to load when this route is called.

createWebHistory: switch from using hash to 
history mode inside the browser (using the HTML5 history API).
*/

const router = createRouter({
  history: createWebHistory(),
  routes: [
      {path: '/', name: 'Home', component: LandingPage},
      {path: '/overview', name: 'Overview', component: Overview},
      {path: '/about', name: 'About', component: About},
      {path: '/getStarted', name: 'GetStarted', component: GetStarted},
      {path: '/configDocs', name: 'ConfigDocs', component: ConfigDocs}
  ]
})

export default router;