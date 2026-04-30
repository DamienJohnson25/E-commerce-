<template>
  <router-link :to="`/product/${product.id}`" class="rec-card">
    <div class="rec-card-image">
      <img :src="product.image_url" :alt="product.name" loading="lazy" />
      
      <div v-if="recommendationLabel" class="adaptive-badge">
        {{ recommendationLabel }}
      </div>
    </div>
    
    <div class="rec-card-body">
      <p class="rec-card-category">{{ product.category }}</p>
      <h4 class="rec-card-name">{{ product.name }}</h4>
      
      <div class="rec-card-footer">
        <span class="rec-card-price">£{{ product.price.toFixed(2) }}</span>
        <span class="rec-card-rating" v-if="product.rating">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="currentColor">
            <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
          </svg>
          {{ product.rating.toFixed(1) }}
        </span>
      </div>
      
      <!-- Debug Score (Highly recommended to keep until you verify the fixes) -->
      <div v-if="product.recommendation_score" class="debug-score">
        Score: {{ product.recommendation_score }}
      </div>
    </div>
  </router-link>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  product: { type: Object, required: true }
})

/**
 * Logic updated to match the 10-point "Genre Lock" scoring 
 * implemented in the backend.
 */
const recommendationLabel = computed(() => {
  const score = props.product.recommendation_score
  if (!score) return null

  // Adjusted thresholds:
  // 14+ = Category Match + High Sales/Rating
  // 10+ = Strict Category Match
  // 5+  = Tag/Price Match
  if (score >= 14) return 'Top Match'
  if (score >= 10) return 'Similar Style'
  if (score >= 5)  return 'Great Value'
  return 'Recommended'
})
</script>

<style scoped>
.rec-card {
  display: flex;
  flex-direction: column;
  background: var(--color-surface);
  border: 1px solid var(--color-border-light);
  border-radius: var(--radius-lg);
  overflow: hidden;
  text-decoration: none;
  color: var(--color-text);
  transition: transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.18s ease;
  flex-shrink: 0;
  width: 180px;
  position: relative;
}

.rec-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.1);
}

.rec-card-image {
  width: 100%;
  aspect-ratio: 1;
  overflow: hidden;
  background: #f8fafc;
  position: relative;
}

.adaptive-badge {
  position: absolute;
  bottom: 8px;
  left: 8px;
  background: rgba(17, 24, 39, 0.8);
  backdrop-filter: blur(4px);
  color: white;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  z-index: 2;
}

.rec-card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s ease;
}

.rec-card:hover .rec-card-image img {
  transform: scale(1.1);
}

.rec-card-body {
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
}

.rec-card-category {
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  color: var(--color-accent);
  margin: 0;
}

.rec-card-name {
  font-size: 0.85rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
  line-height: 1.3;
  height: 2.6em;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.rec-card-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: auto;
  padding-top: 8px;
}

.rec-card-price {
  font-size: 0.95rem;
  font-weight: 800;
  color: #0f172a;
}

.rec-card-rating {
  display: flex;
  align-items: center;
  gap: 3px;
  font-size: 0.75rem;
  font-weight: 600;
  color: #64748b;
}

.rec-card-rating svg {
  color: #f59e0b;
}

.debug-score {
  font-size: 0.6rem;
  color: #94a3b8;
  margin-top: 4px;
  font-family: monospace;
  border-top: 1px dashed #e2e8f0;
  padding-top: 4px;
}
</style>
