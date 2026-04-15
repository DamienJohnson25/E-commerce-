<template>
  <div class="container detail-page">
    <!-- Loading -->
    <div v-if="loading" class="empty-state">
      <div class="spinner"></div>
      <p>Loading product...</p>
    </div>

    <!-- Not Found -->
    <div v-else-if="!product" class="empty-state">
      <span style="font-size: 2.5rem;">😔</span>
      <h3>Product not found</h3>
      <router-link to="/products" class="btn btn-outline">Back to Shop</router-link>
    </div>

    <!-- Product Detail -->
    <div v-else class="detail-layout">
      <div class="detail-image-wrap">
        <img :src="product.image_url" :alt="product.name" class="detail-image" />
        <span v-if="product.featured" class="featured-tag">Featured</span>
      </div>

      <div class="detail-info">
        <router-link to="/products" class="back-link">← Back to Shop</router-link>

        <span class="detail-category">{{ product.category }}</span>
        <h1 class="detail-title">{{ product.name }}</h1>

        <div class="detail-rating">
          <span class="stars">
            {{ '★'.repeat(Math.round(product.rating || 0)) }}
            {{ '☆'.repeat(5 - Math.round(product.rating || 0)) }}
          </span>
          <span class="rating-num">{{ product.rating || 0 }} / 5</span>
        </div>

        <p class="detail-price">{{ formatPrice(product.price) }}</p>
        <p class="detail-desc">{{ product.description }}</p>

        <div class="stock-status" :class="product.stock > 0 ? 'in-stock' : 'out-of-stock'">
          <span class="stock-dot"></span>
          {{ product.stock > 0 ? `${product.stock} in stock` : 'Out of stock' }}
        </div>

        <div class="detail-actions">
          <div class="qty-selector">
            <button class="qty-btn" @click="quantity > 1 && quantity--">−</button>
            <span class="qty-value">{{ quantity }}</span>
            <button class="qty-btn" @click="quantity < product.stock && quantity++">+</button>
          </div>
          <button class="btn btn-primary btn-lg flex-1" @click="handleAddToCart" :disabled="product.stock === 0">
            {{ product.stock === 0 ? 'Out of Stock' : 'Add to Cart' }}
          </button>
        </div>

        <!-- Features -->
        <div class="detail-features">
          <div class="feature-item">
            <span class="feature-icon">🚚</span>
            <div>
              <strong>Free Shipping</strong>
              <p>On orders over £50</p>
            </div>
          </div>
          <div class="feature-item">
            <span class="feature-icon">↩️</span>
            <div>
              <strong>Easy Returns</strong>
              <p>30-day return policy</p>
            </div>
          </div>
          <div class="feature-item">
            <span class="feature-icon">🔒</span>
            <div>
              <strong>Secure Checkout</strong>
              <p>Encrypted payment</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Recommendations -->
    <div v-if="recommendations && recommendations.length" class="recommendations-section">
      <h2>🔥 You might also like</h2>

      <div class="recommendations-row">
        <div
          v-for="item in recommendations"
          :key="item.id"
          class="recommend-card"
          @click="$router.push({ name: 'ProductDetail', params: { id: item.id } })"
        >
          <div class="img-wrap">
            <img :src="item.image_url || item.image" class="recommend-img" />
            <button
              class="quick-add"
              @click.stop="store.addToCart(item.id, 1)"
            >
              + Add
            </button>
          </div>

          <h4>{{ item.name || item.title }}</h4>

          <div class="mini-rating">
            {{ '★'.repeat(Math.round(item.rating || 0)) }}
            {{ '☆'.repeat(5 - Math.round(item.rating || 0)) }}
          </div>

          <p>{{ formatPrice(item.price) }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useShopStore } from '../store/index.js'

const route = useRoute()
const store = useShopStore()

const product = ref(null)
const recommendations = ref([])
const loading = ref(true)
const quantity = ref(1)

// ✅ Currency formatter (GBP)
const formatPrice = (price) => {
  return new Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency: 'GBP'
  }).format(price || 0)
}

async function fetchProduct(id) {
  loading.value = true
  product.value = null
  recommendations.value = []

  try {
    const res = await fetch(`/api/products/${id}`)
    if (res.ok) product.value = await res.json()

    const recRes = await fetch(`/api/products/${id}/recommendations`)
    if (recRes.ok) recommendations.value = await recRes.json()
  } catch (err) {
    console.error('Failed to load product:', err)
  } finally {
    loading.value = false
  }
}

// Initial fetch
fetchProduct(route.params.id)

// Watch for route changes
watch(() => route.params.id, (newId) => {
  if (newId) fetchProduct(newId)
})

function handleAddToCart() {
  if (product.value) store.addToCart(product.value.id, quantity.value)
}
</script>

<style scoped>
.detail-page {
  padding-top: var(--space-lg);
}
.detail-layout { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-3xl); align-items: start; }
.detail-image-wrap { position: relative; border-radius: var(--radius-lg); overflow: hidden; background: var(--color-border-light); }
.detail-image { width: 100%; aspect-ratio: 1; object-fit: cover; }
.featured-tag { position: absolute; top: 16px; left: 16px; padding: 6px 14px; background: var(--color-accent); color: white; font-size: 0.75rem; border-radius: var(--radius-full); }
.detail-info { display: flex; flex-direction: column; gap: var(--space-md); }
.detail-title { font-size: 1.8rem; font-weight: 700; }
.detail-price { font-size: 1.8rem; font-weight: 700; }
.recommendations-section { margin-top: var(--space-3xl); }
.recommendations-row { display: flex; gap: var(--space-md); overflow-x: auto; padding-bottom: 10px; }
.recommend-card { min-width: 160px; flex-shrink: 0; cursor: pointer; text-align: center; }
.img-wrap { position: relative; }
.recommend-img { width: 100%; height: 120px; object-fit: cover; border-radius: var(--radius-md); }
.quick-add { position: absolute; bottom: 8px; left: 50%; transform: translateX(-50%) translateY(10px); opacity: 0; background: var(--color-accent); color: white; border: none; padding: 6px 10px; font-size: 0.75rem; border-radius: var(--radius-full); transition: all 0.2s ease; }
.img-wrap:hover .quick-add { opacity: 1; transform: translateX(-50%) translateY(0); }
.mini-rating { font-size: 0.75rem; color: var(--color-warning); }
@media (max-width: 768px) { .detail-layout { grid-template-columns: 1fr; } }
</style>

