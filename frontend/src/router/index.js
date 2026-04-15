import { createRouter, createWebHistory } from 'vue-router'

// Import views
import HomeView from '../views/HomeView.vue'
import ProductsView from '../views/ProductsView.vue'
import ProductDetail from '../views/ProductDetail.vue'
import CartView from '../views/CartView.vue'
import CheckoutView from '../views/CheckoutView.vue'
import OrderConfirmation from '../views/OrderConfirmation.vue'
import Register from '../views/RegisterView.vue'
import Login from '../views/LoginView.vue'
import { useShopStore } from '../store/index.js'

const routes = [
  { path: '/', name: 'home', component: HomeView, meta: { title: 'ShopVue — Home' } },
  { path: '/products', name: 'products', component: ProductsView, meta: { title: 'ShopVue — Products' } },

  {
    path: '/product/:id',
    name: 'ProductDetail',
    component: ProductDetail,
    meta: { title: 'ShopVue — Product' },
    props: true
  },

  { path: '/cart', name: 'cart', component: CartView, meta: { title: 'ShopVue — Cart' } },
  { path: '/checkout', name: 'checkout', component: CheckoutView, meta: { title: 'ShopVue — Checkout' } },
  { path: '/order/:id', name: 'order-confirmation', component: OrderConfirmation, meta: { title: 'ShopVue — Order Confirmed' } },
  { path: '/register', name: 'register', component: Register, meta: { title: 'ShopVue — Register' } },
  { path: '/login', name: 'login', component: Login, meta: { title: 'ShopVue — Login' } },
  {
    path: '/account',
    name: 'account',
    component: () => import('../views/AccountView.vue'),
    meta: { title: 'ShopVue — My Account' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  }
})

// ✅ FIXED AUTH GUARD
router.beforeEach((to, from, next) => {
  const store = useShopStore()

  // allow public pages
  const publicPaths = ['/', '/register', '/login']

  // allow product browsing WITHOUT login
  if (to.path.startsWith('/products') || to.path.startsWith('/product')) {
    return next()
  }

  if (publicPaths.includes(to.path)) return next()

  if (!store.isLoggedIn) return next('/login')

  next()
})

// Update page title
router.afterEach((to) => {
  document.title = to.meta.title || 'ShopVue'
})

export default router
