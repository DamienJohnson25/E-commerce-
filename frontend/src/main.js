/**
 * main.js — The Application Entry Point
 * ========================================
 * This is where our Vue app is "born." We plug in the router
 * (navigation), the store (shared memory), and mount it to
 * the HTML page.
 *
 * Analogy: This is like opening the restaurant doors on day one —
 * the chef (store), the signage (router), and the space (App.vue)
 * all come together.
 */

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router/index.js'
import './assets/main.css'

const app = createApp(App)

// Pinia = our shared brain (state management)
app.use(createPinia())

// Router = our navigation system
app.use(router)

// Mount the app to the <div id="app"> in index.html
app.mount('#app')
