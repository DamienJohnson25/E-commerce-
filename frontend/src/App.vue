<!--
  App.vue — The Root Component
  ==============================
  This is the "frame" that holds everything together.
  The NavBar is always at the top, the <router-view> swaps
  page content based on the URL, and the footer stays at the bottom.
-->

<template>
  <div class="app">
    <NavBar />
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="page" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <FooterBar />

    <!-- Toast Notification -->
    <transition name="page">
      <div v-if="store.toast" class="toast">
        {{ store.toast }}
      </div>
    </transition>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useShopStore } from './store/index.js'
import NavBar from './components/NavBar.vue'
import FooterBar from './components/FooterBar.vue'

const store = useShopStore()

// Load initial data when the app starts
// Like turning on the lights and checking inventory before opening
onMounted(async () => {
  await Promise.all([
    store.fetchProducts(),
    store.fetchCategories(),
    store.fetchCart()
  ])
})
</script>

<style>
.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex: 1;
  padding-top: var(--space-lg);
  padding-bottom: var(--space-3xl);
}
</style>
