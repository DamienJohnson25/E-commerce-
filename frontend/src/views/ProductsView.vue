<template>
  <div class="container">
    <h1>Shop</h1>

    <!-- ✅ FILTER BAR -->
    <div class="filters">
      <input
        type="text"
        placeholder="Search..."
        v-model="store.searchQuery"
      />

      <select v-model="store.selectedCategory">
        <option value="">All Categories</option>
        <option>Electronics</option>
        <option>Clothing</option>
        <option>Home & Kitchen</option>
        <option>Books</option>
        <option>Accessories</option>
      </select>

      <input
        type="number"
        placeholder="Min £"
        v-model="store.minPrice"
      />

      <input
        type="number"
        placeholder="Max £"
        v-model="store.maxPrice"
      />

      <button @click="applyFilters">Apply</button>
    </div>

    <!-- Loading -->
    <p v-if="loading">Loading products...</p>

    <!-- Products -->
    <div class="products-grid" v-if="!loading && products.length">
      <ProductCard
        v-for="product in products"
        :key="product.id"
        :product="product"
      />
    </div>

    <p v-if="!loading && products.length === 0">
      No products found.
    </p>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useShopStore } from '../store/index.js'
import ProductCard from '../components/ProductCard.vue'

const store = useShopStore()
const loading = ref(true)

// ✅ USE FILTERED PRODUCTS
const products = computed(() => store.featuredProducts || [])

function applyFilters() {
  store.searchProducts()
}

onMounted(async () => {
  await store.fetchProducts()
  loading.value = false
})
</script>

<style scoped>
.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}

/* ✅ SIMPLE CLEAN FILTER UI */
.filters {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.filters input,
.filters select {
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
}

.filters button {
  padding: 6px 12px;
  border: none;
  background: black;
  color: white;
  border-radius: 6px;
  cursor: pointer;
}
</style>
