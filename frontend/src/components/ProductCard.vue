<template>
  <router-link
    :to="{ name: 'ProductDetail', params: { id: product.id } }"
    class="product-card"
  >
    <div class="card-image-wrap">
      <img :src="product.image" :alt="product.title" class="card-image" />
      <span v-if="product.featured" class="featured-tag">Featured</span>
    </div>

    <div class="card-body">
      <div class="card-category">{{ product.category }}</div>
      <div class="card-title">{{ product.title }}</div>
      <div class="card-desc">{{ product.description }}</div>

      <div class="card-footer">
        <!-- ✅ UPDATED PRICE FORMAT -->
        <div class="card-price">{{ formatPrice(product.price) }}</div>

        <div class="card-rating">
          <span v-for="n in Math.floor(product.rating)" :key="n" class="star">★</span>
        </div>
      </div>

      <button class="card-btn" @click.stop="addToCart(product)">Add to Cart</button>
    </div>
  </router-link>
</template>

<script>
import { useShopStore } from '../store/index.js'

export default {
  name: 'ProductCard',
  props: {
    product: { type: Object, required: true }
  },
  setup() {
    const shopStore = useShopStore()

    function addToCart(product) {
      shopStore.addToCart(product.id, 1)
    }

    // ✅ NEW: Currency formatter (GBP)
    function formatPrice(price) {
      return new Intl.NumberFormat('en-GB', {
        style: 'currency',
        currency: 'GBP'
      }).format(price || 0)
    }

    return { addToCart, formatPrice }
  }
}
</script>



<style scoped>
.product-card {
  cursor: pointer;
  display: flex;
  flex-direction: column;
  margin-bottom: 20px;
  border: 1px solid #ddd;
  padding: 10px;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  text-decoration: none; /* ensures router-link text is normal */
  color: inherit;
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
}

.card-image-wrap {
  position: relative;
  overflow: visible;
}

.card-image {
  width: 100%;
  height: auto;
  display: block;
}

.featured-tag {
  position: absolute;
  top: 12px;
  left: 12px;
  padding: 4px 10px;
  background: #ff4c3b;
  color: white;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: uppercase;
  border-radius: 9999px;
}

.card-body {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 10px;
}

.card-category {
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  color: #ff4c3b;
}

.card-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #333;
}

.card-desc {
  font-size: 0.95rem;
  color: #555;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}

.card-price {
  font-size: 1.1rem;
  font-weight: 700;
  color: #333;
}

.card-rating {
  color: #f5a623;
  font-size: 0.9rem;
}

.star {
  margin-right: 2px;
}

.card-btn {
  margin-top: 10px;
  padding: 8px;
  background: #ff4c3b;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 600;
}
</style>
