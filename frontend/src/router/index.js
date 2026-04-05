/**
 * router/index.js — Navigation Configuration
 * =============================================
 * The router is like ROAD SIGNS in our app. Each route maps
 * a URL to a "view" (a full-page component).
 *
 * When a user clicks a link to /cart, the router swaps in
 * the CartView component — no full page reload needed!
 */

import { createRouter, createWebHistory } from 'vue-router'

// Import all our "pages" (views)
import HomeView from '../views/HomeView.vue'
import ProductsView from '../views/ProductsView.vue'
import ProductDetail from '../views/ProductDetail.vue'
import CartView from '../views/CartView.vue'
import CheckoutView from '../views/CheckoutView.vue'
import OrderConfirmation from '../views/OrderConfirmation.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    meta: { title: 'ShopVue — Home' }
  },
  {
    path: '/products',
    name: 'products',
    component: ProductsView,
    meta: { title: 'ShopVue — Products' }
  },
  {
    path: '/product/:id',
    name: 'product-detail',
    component: ProductDetail,
    meta: { title: 'ShopVue — Product' }
  },
  {
    path: '/cart',
    name: 'cart',
    component: CartView,
    meta: { title: 'ShopVue — Cart' }
  },
  {
    path: '/checkout',
    name: 'checkout',
    component: CheckoutView,
    meta: { title: 'ShopVue — Checkout' }
  },
  {
    path: '/order/:id',
    name: 'order-confirmation',
    component: OrderConfirmation,
    meta: { title: 'ShopVue — Order Confirmed' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  // Scroll to top on every page change
  scrollBehavior() {
    return { top: 0 }
  }
})

// Update page title on navigation
router.afterEach((to) => {
  document.title = to.meta.title || 'ShopVue'
})

export default router
