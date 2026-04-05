<!--
  ProductCard.vue — Reusable Product Display Card
  ==================================================
  This is a LEGO piece — one card for one product.
  Used on the home page and the products page.
  
  Props:
    - product: The product object to display
-->

<template>
  <article class="product-card card" @click="goToProduct">
    <!-- Product Image -->
    <div class="card-image-wrap">
      <img
        :src="product.image_url"
        :alt="product.name"
        class="card-image"
        loading="lazy"
      />
      <span v-if="product.featured" class="featured-tag">Featured</span>
    </div>

    <!-- Product Info -->
    <div class="card-body">
      <span class="card-category">{{ product.category }}</span>
      <h3 class="card-title">{{ product.name }}</h3>
      <p class="card-desc">{{ truncate(product.description, 80) }}</p>

      <div class="card-footer">
        <span class="card-price">${{ product.price.toFixed(2) }}</span>
        <div class="card-rating">
          <span class="star">★</span>
          <span>{{ product.rating }}</span>
        </div>
      </div>

      <button
        class="btn btn-primary btn-sm card-btn"
        @click.stop="addToCart"
        :disabled="product.stock === 0"
      >
        {{ product.stock === 0 ? 'Out of Stock' : 'Add to Cart' }}
      </button>
    </div>
  </article>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useShopStore } from '../store/index.js'

const props = defineProps({
  product: { type: Object, required: true }
})

const router = useRouter()
const store = useShopStore()

function goToProduct() {
  router.push(`/product/${props.product.id}`)
}

function addToCart() {
  store.addToCart(props.product.id)
}

function truncate(text, max) {
  return text.length > max ? text.substring(0, max) + '…' : text
}
</script>

<style scoped>
.product-card {
  cursor: pointer;
  display: flex;
  flex-direction: column;
  transition: transform 0.3s var(--ease), box-shadow 0.3s var(--ease);
}

.product-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.card-image-wrap {
  position: relative;
  aspect-ratio: 4 / 3;
  overflow: hidden;
  background: var(--color-border-light);
}

.card-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s var(--ease);
}

.product-card:hover .card-image {
  transform: scale(1.05);
}

.featured-tag {
  position: absolute;
  top: 12px;
  left: 12px;
  padding: 4px 10px;
  background: var(--color-accent);
  color: white;
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  border-radius: var(--radius-full);
}

.card-body {
  padding: var(--space-md) var(--space-lg) var(--space-lg);
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
  flex: 1;
}

.card-category {
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-accent);
}

.card-title {
  font-family: var(--font-heading);
  font-size: 1.1rem;
  font-weight: 600;
  line-height: 1.3;
  color: var(--color-text);
}

.card-desc {
  font-size: 0.85rem;
  color: var(--color-text-muted);
  line-height: 1.5;
}

.card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: var(--space-sm);
}

.card-price {
  font-size: 1.15rem;
  font-weight: 700;
  color: var(--color-text);
}

.card-rating {
  display: flex;
  align-items: center;
  gap: 3px;
  font-size: 0.85rem;
  color: var(--color-text-muted);
}

.star {
  color: var(--color-warning);
}

.card-btn {
  margin-top: var(--space-sm);
  width: 100%;
}
</style>
