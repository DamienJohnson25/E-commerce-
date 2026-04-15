<!--
  HomeView.vue — The Landing Page
  =================================
  The first thing shoppers see. Shows a hero banner
  and a grid of featured products.
-->

<template>
  <div class="home">
    <!-- Hero Section -->
    <section class="hero">
      <div class="container hero-inner">
        <span class="hero-eyebrow">New Season Collection</span>
        <h1 class="hero-title">Curated Goods<br/>for Everyday Life</h1>
        <p class="hero-subtitle">
          Discover thoughtfully selected products — from electronics to
          home essentials — built to last and designed to delight.
         
      
     
        </p>
        <router-link to="/products" class="btn btn-primary btn-lg">
          Browse the Shop
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
            <path d="M5 12h14M12 5l7 7-7 7"/>
          </svg>
        </router-link>
      </div>
    </section>

    <!-- Featured Products -->
    <section class="container section">
      <div class="section-header">
        <h2 class="section-title">Featured Picks</h2>
        <router-link to="/products" class="section-link">
          View all →
        </router-link>
      </div>
      <div v-if="store.loading" class="loading-text">Loading products...</div>
      <div v-else class="product-grid">
       <ProductCard
        v-for="product in (store.featuredProducts || []).slice(0, 4)"
        :key="product.id"
        :product="product"

        />
      </div>
    </section>

    <!-- Categories Section -->
    <section class="container section">
      <h2 class="section-title" style="text-align: center; margin-bottom: var(--space-xl);">
        Shop by Category
      </h2>
      <div class="category-grid">
        <router-link
          v-for="cat in store.categories"
          :key="cat"
          :to="{ path: '/products', query: { category: cat } }"
          class="category-card"
        >
          <span class="category-icon">{{ getCategoryIcon(cat) }}</span>
          <span class="category-name">{{ cat }}</span>
        </router-link>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useShopStore } from '../store/index.js'
import ProductCard from '../components/ProductCard.vue'

const store = useShopStore()

function getCategoryIcon(category) {
  const icons = {
    'Electronics': '⚡',
    'Clothing': '👕',
    'Home & Kitchen': '🏠',
    'Books': '📚',
    'Accessories': '⌚'
  }
  return icons[category] || '📦'
}
</script>

<style scoped>
/* ─── Hero ──────────────────────────────────────────────── */
.hero {
  background:
    linear-gradient(135deg, #FAF8F5 0%, #F0ECE8 50%, #E8E4E0 100%);
  padding: var(--space-3xl) 0;
  margin-bottom: var(--space-2xl);
  border-bottom: 1px solid var(--color-border-light);
}

.hero-inner {
  max-width: 640px;
}

.hero-eyebrow {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--color-accent);
  margin-bottom: var(--space-md);
  padding: 4px 12px;
  background: var(--color-accent-light);
  border-radius: var(--radius-full);
}

.hero-title {
  font-family: var(--font-heading);
  font-size: clamp(2rem, 5vw, 3.2rem);
  font-weight: 700;
  line-height: 1.15;
  color: var(--color-text);
  margin-bottom: var(--space-md);
}

.hero-subtitle {
  font-size: 1.05rem;
  line-height: 1.7;
  color: var(--color-text-muted);
  margin-bottom: var(--space-xl);
  max-width: 520px;
}

/* ─── Sections ──────────────────────────────────────────── */
.section {
  margin-bottom: var(--space-3xl);
}

.section-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  margin-bottom: var(--space-xl);
}

.section-title {
  font-family: var(--font-heading);
  font-size: 1.6rem;
  font-weight: 700;
}

.section-link {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--color-accent);
  transition: color 0.2s;
}

.section-link:hover {
  color: var(--color-accent-hover);
}

.loading-text {
  text-align: center;
  color: var(--color-text-muted);
  padding: var(--space-2xl);
}

/* ─── Product Grid ──────────────────────────────────────── */
.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: var(--space-lg);
}

/* ─── Category Grid ─────────────────────────────────────── */
.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: var(--space-md);
}

.category-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-xl) var(--space-lg);
  background: var(--color-surface);
  border: 1.5px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  transition: all 0.25s var(--ease);
}

.category-card:hover {
  border-color: var(--color-accent);
  background: var(--color-accent-light);
  transform: translateY(-2px);
}

.category-icon {
  font-size: 1.8rem;
}

.category-name {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--color-text);
}
</style>
