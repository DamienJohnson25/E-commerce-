<!--
  RecommendationsRow.vue — Horizontally scrollable recommendations strip
  ========================================================================
  Props:
    - title:        Section heading e.g. "You may also like"
    - productId:    Pass on product detail page
    - sessionId:    Pass on home page / cart (uses cart contents as context)
    - filterType:   'category' | 'brand' | 'price_range' | 'trending' | 'tags'
    - filterValue:  The value to filter by (e.g. 'Electronics', 'Sony', '49.99', 'wireless,gaming')
    - limit:        Max products to show (default 8)
-->
<template>
  <section class="rec-section" v-if="recommendations.length > 0 || loading">
    <div class="rec-header">
      <h2 class="rec-title">{{ title }}</h2>
    </div>

    <!-- Loading skeleton -->
    <div v-if="loading" class="rec-track">
      <div v-for="n in 5" :key="n" class="rec-skeleton" />
    </div>

    <!-- Recommendations -->
    <div v-else class="rec-track" ref="trackRef">
      <RecommendationCard
        v-for="product in recommendations"
        :key="product.id"
        :product="product"
      />
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import RecommendationCard from './RecommendationCard.vue'

const props = defineProps({
  title:       { type: String,            default: 'You may also like' },
  productId:   { type: Number,            default: null },
  sessionId:   { type: String,            default: null },
  filterType:  { type: String,            default: null },   // category | brand | price_range | trending | tags
  filterValue: { type: [String, Number],  default: null },
  limit:       { type: Number,            default: 8 }
})

const recommendations = ref([])
const loading = ref(true)
const trackRef = ref(null)

async function fetchRecommendations() {
  loading.value = true
  try {
    const params = new URLSearchParams({ limit: props.limit })

    if (props.productId)   params.append('product_id',    props.productId)
    if (props.sessionId)   params.append('session_id',    props.sessionId)
    if (props.filterType)  params.append('filter_type',   props.filterType)
    if (props.filterValue !== null && props.filterValue !== undefined) {
      params.append('filter_value', props.filterValue)
    }

    const res = await fetch(`/api/recommendations?${params}`)
    if (!res.ok) throw new Error('Failed to fetch recommendations')
    recommendations.value = await res.json()
  } catch (err) {
    console.error('RecommendationsRow error:', err)
    recommendations.value = []
  } finally {
    loading.value = false
  }
}

onMounted(fetchRecommendations)

// Re-fetch if productId or filterValue changes (e.g. navigating between product pages)
watch(() => [props.productId, props.filterValue], fetchRecommendations)
</script>

<style scoped>
.rec-section {
  padding: var(--space-2xl) 0;
  border-top: 1px solid var(--color-border-light);
}

.rec-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-lg);
}

.rec-title {
  font-family: var(--font-heading);
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--color-text);
  margin: 0;
}

/* Scrollable track */
.rec-track {
  display: flex;
  gap: var(--space-md);
  overflow-x: auto;
  padding-bottom: var(--space-sm);
  scroll-snap-type: x mandatory;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}

.rec-track::-webkit-scrollbar {
  display: none;
}

.rec-track > * {
  scroll-snap-align: start;
  flex-shrink: 0;
}

/* Loading skeleton cards */
.rec-skeleton {
  width: 180px;
  aspect-ratio: 0.85;
  border-radius: var(--radius-lg);
  background: linear-gradient(
    90deg,
    var(--color-border-light) 25%,
    var(--color-border) 50%,
    var(--color-border-light) 75%
  );
  background-size: 200% 100%;
  animation: shimmer 1.4s infinite;
  flex-shrink: 0;
}

@keyframes shimmer {
  0%   { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

@media (max-width: 640px) {
  .rec-title { font-size: 1.05rem; }
}
</style>
