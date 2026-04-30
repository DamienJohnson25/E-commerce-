<template>
  <div class="container detail-page">
    <div v-if="product">
      <div class="detail-layout">
        <!-- PRODUCT VISUALS -->
        <div class="product-visuals">
          <img :src="product.image_url" :alt="product.name" class="main-image" />
        </div>

        <!-- PRODUCT INFO -->
        <div class="product-info">
          <p class="category-breadcrumb">{{ product.category }}</p>
          <h1 class="product-title">{{ product.name }}</h1>
          
          <div class="product-meta">
            <span class="price-tag">£{{ product.price.toFixed(2) }}</span>
            <span v-if="product.brand" class="brand-tag">| {{ product.brand }}</span>
          </div>

          <p class="description">{{ product.description }}</p>

          <!-- ── RESTORED QUANTITY & CART CONTROLS ── -->
          <div class="purchase-zone">
            <div class="quantity-controls">
              <button 
                @click="updateQuantity(-1)" 
                class="qty-btn" 
                :disabled="quantity <= 1"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
              </button>
              
              <span class="qty-number">{{ quantity }}</span>
              
              <button 
                @click="updateQuantity(1)" 
                class="qty-btn"
                :disabled="quantity >= (product.stock || 99)"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3">
                  <line x1="12" y1="5" x2="12" y2="19"></line>
                  <line x1="5" y1="12" x2="19" y2="12"></line>
                </svg>
              </button>
            </div>

            <button @click="addToCart" class="add-to-cart-btn">
              Add to Cart
            </button>
          </div>
          
          <p v-if="product.stock <= 5" class="stock-warning">
            Only {{ product.stock }} left in stock!
          </p>
        </div>
      </div>

      <!-- RECOMMENDATIONS SECTION -->
      <div class="recommendations-container">
        <RecommendationsRow
          :title="`More ${product.category}`"
          :productId="product.id"
          filterType="category"
          :filterValue="product.category"
        />

        <RecommendationsRow
          :title="`In a Similar Price Range`"
          :productId="product.id"
          filterType="price_range"
          :filterValue="product.price"
        />
        
        <!-- ... other rows remain the same ... -->
      </div>
    </div>

    <!-- LOADING STATE -->
    <div v-else-if="loading" class="page-loading">
      <div class="page-skeleton" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useShopStore } from '../store/index.js' // Assuming you have a Pinia/Vuex store
import RecommendationsRow from '../components/RecommendationsRow.vue'

const route = useRoute()
const store = useShopStore()

const product = ref(null)
const loading = ref(true)
const quantity = ref(1)

async function loadPageData() {
  loading.value = true
  quantity.value = 1 // Reset quantity on new product load
  try {
    const res = await fetch(`/api/products/${route.params.id}`)
    if (res.ok) product.value = await res.json()
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
}

function updateQuantity(diff) {
  const next = quantity.value + diff
  if (next >= 1 && next <= (product.value.stock || 99)) {
    quantity.value = next
  }
}

function addToCart() {
  store.addToCart(product.value.id, quantity.value)
}

onMounted(loadPageData)
watch(() => route.params.id, loadPageData)
</script>

<style scoped>
.purchase-zone {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-top: 2rem;
}

.quantity-controls {
  display: flex;
  align-items: center;
  background: #f1f5f9;
  border-radius: 12px;
  padding: 4px;
  border: 1px solid #e2e8f0;
}

.qty-btn {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  color: #1e293b;
  transition: all 0.2s;
  box-shadow: 0 2px 4px rgba(0,0,0,0.05);
}

.qty-btn:hover:not(:disabled) {
  background: #f8fafc;
  color: #6366f1;
}

.qty-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.qty-number {
  padding: 0 1.25rem;
  font-weight: 700;
  font-size: 1.1rem;
  min-width: 50px;
  text-align: center;
}

.add-to-cart-btn {
  flex: 1;
  height: 48px;
  background: #1e293b;
  color: white;
  border: none;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.1s active;
}

.add-to-cart-btn:hover {
  background: #0f172a;
}

.add-to-cart-btn:active {
  transform: scale(0.98);
}

.stock-warning {
  margin-top: 1rem;
  font-size: 0.85rem;
  color: #e11d48;
  font-weight: 600;
}


</style>

<style scoped>
.detail-page { padding: 2rem 0; }

.detail-layout {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  margin-bottom: 5rem;
}

.main-image {
  width: 100%;
  aspect-ratio: 1;
  object-fit: cover;
  border-radius: 12px;
  background: #f8fafc;
}

.category-breadcrumb {
  text-transform: uppercase;
  font-size: 0.75rem;
  font-weight: 700;
  color: #6366f1;
  letter-spacing: 0.05em;
  margin-bottom: 0.5rem;
}

.product-title {
  font-size: 2.5rem;
  font-weight: 800;
  color: #1e293b;
  line-height: 1.1;
  margin-bottom: 1.5rem;
}

.price-tag {
  font-size: 1.75rem;
  font-weight: 700;
  color: #0f172a;
}

.description {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #475569;
  margin: 2rem 0;
}

.add-to-cart-btn {
  background: #1e293b;
  color: white;
  padding: 1rem 2.5rem;
  border-radius: 8px;
  font-weight: 600;
  border: none;
  cursor: pointer;
}

.recommendations-container {
  border-top: 1px solid #e2e8f0;
  padding-top: 3rem;
}

/* Skeleton animation */
.page-skeleton {
  width: 100%;
  height: 400px;
  background: #f1f5f9;
  border-radius: 12px;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

@media (max-width: 768px) {
  .detail-layout { grid-template-columns: 1fr; gap: 2rem; }
  .product-title { font-size: 1.75rem; }
}
</style>