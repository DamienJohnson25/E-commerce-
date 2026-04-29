<!--
  ProductDetail.vue — Single Product Page
  ==========================================
  Shows full details for one product with add-to-cart.
  Like picking up an item in a store and reading the back of the box.
-->

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
      <!-- Image -->
      <div class="detail-image-wrap">
        <img :src="product.image_url" :alt="product.name" class="detail-image" />
        <span v-if="product.featured" class="featured-tag">Featured</span>
      </div>

      <!-- Info -->
      <div class="detail-info">
        <router-link to="/products" class="back-link">
          ← Back to Shop
        </router-link>

        <span class="detail-category">{{ product.category }}</span>
        <h1 class="detail-title">{{ product.name }}</h1>

        <div class="detail-rating">
          <span class="stars">{{ '★'.repeat(Math.round(product.rating)) }}{{ '☆'.repeat(5 - Math.round(product.rating)) }}</span>
          <span class="rating-num">{{ product.rating }} / 5</span>
        </div>

        <p class="detail-price">£{{ product.price.toFixed(2) }}</p>

        <p class="detail-desc">{{ product.description }}</p>

        <!-- Stock Status -->
        <div class="stock-status" :class="product.stock > 0 ? 'in-stock' : 'out-of-stock'">
          <span class="stock-dot"></span>
          {{ product.stock > 0 ? `${product.stock} in stock` : 'Out of stock' }}
        </div>

        <!-- Quantity Selector + Add to Cart -->
        <div class="detail-actions">
          <div class="qty-selector">
            <button class="qty-btn" @click="quantity > 1 && quantity--">−</button>
            <span class="qty-value">{{ quantity }}</span>
            <button class="qty-btn" @click="quantity < product.stock && quantity++">+</button>
          </div>
          <button
            class="btn btn-primary btn-lg flex-1"
            @click="handleAddToCart"
            :disabled="product.stock === 0"
          >
            {{ product.stock === 0 ? 'Out of Stock' : 'Add to Cart' }}
          </button>
        </div>

        <!-- Features List -->
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
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useShopStore } from '../store/index.js'

const route = useRoute()
const store = useShopStore()
const product = ref(null)
const loading = ref(true)
const quantity = ref(1)

onMounted(async () => {
  try {
    const res = await fetch(`/api/products/${route.params.id}`)
    if (res.ok) {
      product.value = await res.json()
    }
  } catch (err) {
    console.error('Failed to load product:', err)
  } finally {
    loading.value = false
  }
})

function handleAddToCart() {
  if (product.value) {
    store.addToCart(product.value.id, quantity.value)
  }
}
</script>

<style scoped>
.detail-page {
  padding-top: var(--space-lg);
}

.detail-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-3xl);
  align-items: start;
}

/* ─── Image ───────────────────────────────────────────── */
.detail-image-wrap {
  position: relative;
  border-radius: var(--radius-lg);
  overflow: hidden;
  background: var(--color-border-light);
}

.detail-image {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
}

.featured-tag {
  position: absolute;
  top: 16px;
  left: 16px;
  padding: 6px 14px;
  background: var(--color-accent);
  color: white;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  border-radius: var(--radius-full);
}

/* ─── Info ────────────────────────────────────────────── */
.detail-info {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.back-link {
  font-size: 0.85rem;
  color: var(--color-text-muted);
  transition: color 0.2s;
  align-self: flex-start;
}

.back-link:hover {
  color: var(--color-accent);
}

.detail-category {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--color-accent);
}

.detail-title {
  font-family: var(--font-heading);
  font-size: 1.8rem;
  font-weight: 700;
  line-height: 1.2;
}

.detail-rating {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
}

.stars {
  color: var(--color-warning);
  letter-spacing: 2px;
}

.rating-num {
  font-size: 0.85rem;
  color: var(--color-text-muted);
}

.detail-price {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--color-text);
}

.detail-desc {
  font-size: 1rem;
  line-height: 1.7;
  color: var(--color-text-muted);
}

/* ─── Stock ───────────────────────────────────────────── */
.stock-status {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: 0.85rem;
  font-weight: 500;
}

.stock-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.in-stock { color: var(--color-success); }
.in-stock .stock-dot { background: var(--color-success); }
.out-of-stock { color: var(--color-danger); }
.out-of-stock .stock-dot { background: var(--color-danger); }

/* ─── Actions ─────────────────────────────────────────── */
.detail-actions {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  margin-top: var(--space-sm);
}

.flex-1 { flex: 1; }

.qty-selector {
  display: flex;
  align-items: center;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-md);
  overflow: hidden;
}

.qty-btn {
  width: 40px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  color: var(--color-text);
  transition: background 0.15s;
}

.qty-btn:hover {
  background: var(--color-border-light);
}

.qty-value {
  width: 40px;
  text-align: center;
  font-weight: 600;
  font-size: 0.95rem;
}

/* ─── Features ────────────────────────────────────────── */
.detail-features {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
  margin-top: var(--space-lg);
  padding-top: var(--space-lg);
  border-top: 1px solid var(--color-border-light);
}

.feature-item {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.feature-icon {
  font-size: 1.3rem;
}

.feature-item strong {
  font-size: 0.85rem;
  display: block;
}

.feature-item p {
  font-size: 0.8rem;
  color: var(--color-text-light);
}

/* ─── Empty State ─────────────────────────────────────── */
.empty-state {
  text-align: center;
  padding: var(--space-3xl);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-md);
  color: var(--color-text-muted);
}

.empty-state h3 {
  font-family: var(--font-heading);
  color: var(--color-text);
}

.spinner {
  width: 32px;
  height: 32px;
  border: 3px solid var(--color-border);
  border-top-color: var(--color-accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* ─── Responsive ──────────────────────────────────────── */
@media (max-width: 768px) {
  .detail-layout {
    grid-template-columns: 1fr;
    gap: var(--space-xl);
  }
}
</style>
