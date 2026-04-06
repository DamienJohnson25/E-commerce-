<!--
  NavBar.vue — The Navigation Bar
  =================================
  Always visible at the top of the page.
  Contains: logo, search bar, and cart icon with count badge.
  
  Analogy: The front desk of the store — first thing you see,
  where you can ask for directions or check your bag.
-->

<template>
  <nav class="navbar">
    <div class="container navbar-inner">
      <!-- Logo / Brand -->
      <router-link to="/" class="navbar-brand">
        <span class="brand-icon">◆</span>
        <span class="brand-text">ShopVue</span>
      </router-link>

      <!-- Navigation Links -->
      <div class="navbar-links">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/products" class="nav-link">Shop</router-link>
        <router-link to="/account" class="nav-link">Account</router-link>
      </div>

      <!-- Search Bar -->
      <div class="navbar-search">
        <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
          <circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" />
        </svg>
       

        <input
          type="text"
          class="search-input"
          placeholder="Search products..."
          :value="store.searchQuery"
          @input="onSearch($event.target.value)"
          @keyup.enter="goToProducts"
        />
      </div>



      <!-- Cart Icon -->
      <router-link to="/cart" class="cart-link">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M6 2L3 6v14a2 2 0 002 2h14a2 2 0 002-2V6l-3-4z" />
          <line x1="3" y1="6" x2="21" y2="6" />
          <path d="M16 10a4 4 0 01-8 0" />
        </svg>
        <span v-if="store.cartItemCount > 0" class="badge cart-badge">
          {{ store.cartItemCount }}
        </span>
      </router-link>
    </div>
  </nav>
</template>

<script setup>
import { useShopStore } from '../store/index.js'
import { useRouter } from 'vue-router'

const store = useShopStore()
const router = useRouter()

let searchTimeout = null

function onSearch(value) {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    store.searchProducts(value)
  }, 300)
}

function goToProducts() {
  router.push('/products')
}
</script>

<style scoped>
.navbar {
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border-light);
  position: sticky;
  top: 0;
  z-index: 100;
  backdrop-filter: blur(12px);
  background: rgba(255, 255, 255, 0.92);
}

.navbar-inner {
  display: flex;
  align-items: center;
  gap: var(--space-lg);
  height: 64px;
}

.navbar-brand {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-family: var(--font-heading);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-text);
  flex-shrink: 0;
}

.brand-icon {
  color: var(--color-accent);
  font-size: 1rem;
}

.navbar-links {
  display: flex;
  gap: var(--space-md);
  flex-shrink: 0;
}

.nav-link {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--color-text-muted);
  transition: color 0.2s;
  padding: var(--space-xs) 0;
  border-bottom: 2px solid transparent;
}

.nav-link:hover,
.nav-link.router-link-active {
  color: var(--color-text);
}

.nav-link.router-link-exact-active {
  border-bottom-color: var(--color-accent);
}

.navbar-search {
  flex: 1;
  max-width: 360px;
  position: relative;
  margin-left: auto;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-text-light);
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 0.5rem 0.75rem 0.5rem 2.5rem;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-full);
  background: var(--color-bg);
  font-size: 0.85rem;
  color: var(--color-text);
  transition: all 0.2s var(--ease);
}

.search-input:focus {
  outline: none;
  border-color: var(--color-accent);
  background: var(--color-surface);
  box-shadow: 0 0 0 3px var(--color-accent-light);
}

.search-input::placeholder {
  color: var(--color-text-light);
}

.cart-link {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  color: var(--color-text);
  transition: background 0.2s;
  flex-shrink: 0;
}

.cart-link:hover {
  background: var(--color-border-light);
}

.cart-badge {
  position: absolute;
  top: 0;
  right: -2px;
}

@media (max-width: 640px) {
  .navbar-links {
    display: none;
  }
  .navbar-search {
    max-width: 200px;
  }
}
</style>
