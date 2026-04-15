import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router/index.js'
import './assets/main.css'
import { useShopStore } from './store/index.js'

const app = createApp(App)

const pinia = createPinia()
app.use(pinia)

app.use(router)

/* ✅ IMPORTANT FIX:
   Use ONE unified initializer instead of calling initAuth + initCart separately
*/
const store = useShopStore()
store.initStore()

app.mount('#app')
