<!--
  ProductsView.vue — The Product Catalog Page
  ==============================================
  Shows all products with category filtering.
  Like walking into the store and browsing the aisles.
-->

<template>
  <div class="products-page container">
    <!-- Page Header -->
    <div class="page-header">
      <h1 class="page-title">The Shop</h1>
      <p class="page-subtitle">
        {{ store.filteredProducts.length }} product{{ store.filteredProducts.length !== 1 ? 's' : '' }}
        <span v-if="store.searchQuery"> matching "{{ store.searchQuery }}"</span>
        <span v-if="activeCategory !== 'all'"> in {{ activeCategory }}</span>
      </p>
    </div>

    <!-- Category Filter Tabs -->
    <div class="filter-bar">
      <button
        class="filter-tab"
        :class="{ active: activeCategory === 'all' }"
        @click="setCategory('all')"
      >
        All
      </button>
      <button
        v-for="cat in store.categories"
        :key="cat"
        class="filter-tab"
        :class="{ active: activeCategory === cat }"
        @click="setCategory(cat)"
      >
        {{ cat }}
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="store.loading" class="empty-state">
      <div class="spinner"></div>
      <p>Loading products...</p>
    </div>

    <!-- Empty State -->
    <div v-else-if="store.filteredProducts.length === 0" class="empty-state">
      <span class="empty-icon">🔍</span>
      <h3>No products found</h3>
      <p>Try a different search or category</p>
      <button class="btn btn-outline" @click="clearFilters">Clear Filters</button>
    </div>

    <!-- Product Grid -->
    <div v-else class="product-grid">
      <ProductCard
        v-for="product in store.filteredProducts"
        :key="product.id"
        :product="product"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useShopStore } from '../store/index.js'
import ProductCard from '../components/ProductCard.vue'

const store = useShopStore()
const route = useRoute()
const router = useRouter()
const activeCategory = ref('all')

onMounted(() => {
  // Check URL for category query param (/products?category=Electronics)
  if (route.query.category) {
    setCategory(route.query.category)
  }
})

// Watch for query param changes
watch(() => route.query.category, (newCat) => {
  if (newCat) {
    activeCategory.value = newCat
    store.selectedCategory = newCat
  }
})

function setCategory(category) {
  activeCategory.value = category
  store.selectedCategory = category
  // Update URL without full page reload
  router.replace({ query: category !== 'all' ? { category } : {} })
}

function clearFilters() {
  store.searchQuery = ''
  setCategory('all')
  store.fetchProducts()
}
</script>

<style scoped>
.products-page {
  padding-top: var(--space-lg);
}

.page-header {
  margin-bottom: var(--space-xl);
}

.page-title {
  font-family: var(--font-heading);
  font-size: 2rem;
  font-weight: 700;
}

.page-subtitle {
  font-size: 0.9rem;
  color: var(--color-text-muted);
  margin-top: var(--space-xs);
}

/* ─── Filter Tabs ─────────────────────────────────────── */
.filter-bar {
  display: flex;
  gap: var(--space-sm);
  margin-bottom: var(--space-xl);
  overflow-x: auto;
  padding-bottom: var(--space-xs);
  -ms-overflow-style: none;
  scrollbar-width: none;
}

.filter-bar::-webkit-scrollbar {
  display: none;
}

.filter-tab {
  padding: 0.5rem 1.1rem;
  border-radius: var(--radius-full);
  font-size: 0.85rem;
  font-weight: 500;
  color: var(--color-text-muted);
  background: var(--color-surface);
  border: 1.5px solid var(--color-border);
  white-space: nowrap;
  transition: all 0.2s var(--ease);
}

.filter-tab:hover {
  border-color: var(--color-text-muted);
  color: var(--color-text);
}

.filter-tab.active {
  background: var(--color-text);
  color: var(--color-surface);
  border-color: var(--color-text);
}

/* ─── Product Grid ──────────────────────────────────────── */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: var(--space-lg);
}

/* ─── Empty State ───────────────────────────────────────── */
.empty-state {
  text-align: center;
  padding: var(--space-3xl) var(--space-lg);
  color: var(--color-text-muted);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-sm);
}

.empty-icon {
  font-size: 2.5rem;
}

.empty-state h3 {
  font-family: var(--font-heading);
  color: var(--color-text);
  font-size: 1.2rem;
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
