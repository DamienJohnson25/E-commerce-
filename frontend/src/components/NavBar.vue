<template>
  <nav class="navbar">
    <div class="container navbar-inner">
      <!-- Logo -->
      <router-link to="/" class="navbar-brand">
        <span class="brand-icon">◆</span>
        <span class="brand-text">ShopVue</span>
      </router-link>

      <!-- Links -->
      <div class="navbar-links">
        <router-link to="/" class="nav-link">Home</router-link>
        <router-link to="/products" class="nav-link">Shop</router-link>
        <router-link to="/account" class="nav-link">Account</router-link>
      </div>

      <!-- 🔍 Search -->
      <div class="navbar-search">
        <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <circle cx="11" cy="11" r="8" />
          <path d="m21 21-4.35-4.35" />
        </svg>

        <input
          type="text"
          class="search-input"
          placeholder="Search products..."
          v-model="searchQuery"
          @input="handleSearch"
        />

        <!-- ✅ DROPDOWN RESULTS -->
        <div v-if="results.length && searchQuery" class="search-dropdown">
          <div
            v-for="item in results"
            :key="item.id"
            class="search-item"
            @click="goToProduct(item.id)"
          >
            <!-- ✅ ADDED IMAGE -->
            <img :src="item.image_url" class="search-img" />

            <!-- ✅ ADDED TEXT BLOCK -->
            <div class="search-info">
              <div class="search-name">{{ item.name }}</div>
              <div class="search-price">£{{ item.price }}</div>
            </div>
          </div>
        </div>
      </div>

      <!-- Cart -->
      <router-link to="/cart" class="cart-link">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
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
import { ref } from 'vue'
import { useShopStore } from '../store/index.js'
import { useRouter } from 'vue-router'

const store = useShopStore()
const router = useRouter()

const searchQuery = ref('')
const results = ref([])

let searchTimeout = null

// 🔍 FETCH SEARCH RESULTS
function handleSearch() {
  clearTimeout(searchTimeout)

  searchTimeout = setTimeout(async () => {
    if (!searchQuery.value) {
      results.value = []
      return
    }

    const res = await fetch(
      `http://localhost:5000/api/products/search?q=${searchQuery.value}`
    )
    const data = await res.json()

    results.value = data.slice(0, 5) // limit results
  }, 300)
}

// 👉 GO TO PRODUCT PAGE
function goToProduct(id) {
  router.push(`/product/${id}`)
  results.value = []
  searchQuery.value = ''
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

/* ✅ ADDED: SEARCH DROPDOWN UI (clean + compact) */
.search-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  background: white;
  border: 1px solid #e5e5e5;
  border-radius: 10px;
  margin-top: 6px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  z-index: 1000;
}

.search-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 10px;
  cursor: pointer;
  transition: background 0.15s ease;
}

.search-item:hover {
  background: #f7f7f7;
}

.search-img {
  width: 28px;
  height: 28px;
  object-fit: cover;
  border-radius: 5px;
}

.search-info {
  display: flex;
  flex-direction: column;
  line-height: 1.2;
}

.search-name {
  font-size: 0.85rem;
  font-weight: 500;
  color: #222;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.search-price {
  font-size: 0.75rem;
  color: #888;
}
</style>
