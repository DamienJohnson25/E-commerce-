<!--
  OrderConfirmation.vue — Order Success Page
  =============================================
  Shown after a successful checkout.
  Like getting a receipt with a big "Thank You!"
-->

<template>
  <div class="container confirm-page">
    <!-- Loading -->
    <div v-if="loading" class="empty-state">
      <div class="spinner"></div>
      <p>Loading order details...</p>
    </div>

    <!-- Not Found -->
    <div v-else-if="!order" class="empty-state">
      <span style="font-size: 2.5rem;">😔</span>
      <h3>Order not found</h3>
      <router-link to="/" class="btn btn-outline">Go Home</router-link>
    </div>

    <!-- Confirmation -->
    <div v-else class="confirm-content">
      <!-- Success Header -->
      <div class="confirm-header">
        <div class="check-circle">
          <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="20 6 9 17 4 12"/>
          </svg>
        </div>
        <h1 class="confirm-title">Order Confirmed!</h1>
        <p class="confirm-subtitle">
          Thank you, {{ order.customer_name }}! Your order <strong>#{{ order.id }}</strong> has been placed.
        </p>
        <p class="confirm-email">
          A confirmation would be sent to <strong>{{ order.customer_email }}</strong>
        </p>
      </div>

      <!-- Order Details Card -->
      <div class="confirm-details card">
        <div class="details-header">
          <div>
            <span class="details-label">Order Number</span>
            <span class="details-value">#{{ order.id }}</span>
          </div>
          <div>
            <span class="details-label">Date</span>
            <span class="details-value">{{ formatDate(order.created_at) }}</span>
          </div>
          <div>
            <span class="details-label">Status</span>
            <span class="status-badge">{{ order.status }}</span>
          </div>
          <div>
            <span class="details-label">Total</span>
            <span class="details-value total">${{ order.total.toFixed(2) }}</span>
          </div>
        </div>

        <!-- Line Items -->
        <div class="order-items">
          <h3 class="items-title">Items Ordered</h3>
          <div v-for="item in order.items" :key="item.id" class="order-item">
            <div class="order-item-info">
              <span class="order-item-name">{{ item.product_name }}</span>
              <span class="order-item-qty">Qty: {{ item.quantity }}</span>
            </div>
            <span class="order-item-price">${{ (item.price * item.quantity).toFixed(2) }}</span>
          </div>
        </div>

        <!-- Shipping Info -->
        <div class="shipping-info">
          <h3 class="items-title">Shipping To</h3>
          <p>{{ order.customer_name }}</p>
          <p>{{ order.address }}</p>
          <p>{{ order.city }}, {{ order.zip_code }}</p>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="confirm-actions">
        <router-link to="/products" class="btn btn-primary btn-lg">
          Continue Shopping
        </router-link>
        <router-link to="/" class="btn btn-outline btn-lg">
          Back to Home
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const order = ref(null)
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await fetch(`/api/orders/${route.params.id}`)
    if (res.ok) {
      order.value = await res.json()
    }
  } catch (err) {
    console.error('Failed to load order:', err)
  } finally {
    loading.value = false
  }
})

function formatDate(dateStr) {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
.confirm-page {
  padding-top: var(--space-xl);
}

.confirm-content {
  max-width: 680px;
  margin: 0 auto;
}

/* ─── Header ──────────────────────────────────────────── */
.confirm-header {
  text-align: center;
  margin-bottom: var(--space-2xl);
}

.check-circle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: var(--color-success-bg);
  color: var(--color-success);
  margin-bottom: var(--space-lg);
}

.confirm-title {
  font-family: var(--font-heading);
  font-size: 2rem;
  margin-bottom: var(--space-sm);
}

.confirm-subtitle {
  font-size: 1rem;
  color: var(--color-text-muted);
}

.confirm-email {
  font-size: 0.85rem;
  color: var(--color-text-light);
  margin-top: var(--space-xs);
}

/* ─── Details Card ────────────────────────────────────── */
.confirm-details {
  padding: var(--space-xl);
}

.details-header {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-md);
  padding-bottom: var(--space-lg);
  border-bottom: 1px solid var(--color-border-light);
}

.details-label {
  display: block;
  font-size: 0.72rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-text-light);
  margin-bottom: 4px;
}

.details-value {
  font-weight: 600;
  font-size: 0.95rem;
}

.details-value.total {
  font-size: 1.1rem;
  color: var(--color-accent);
}

.status-badge {
  display: inline-block;
  padding: 3px 10px;
  background: var(--color-success-bg);
  color: var(--color-success);
  font-size: 0.78rem;
  font-weight: 600;
  border-radius: var(--radius-full);
  text-transform: capitalize;
}

/* ─── Items List ──────────────────────────────────────── */
.order-items, .shipping-info {
  padding-top: var(--space-lg);
}

.items-title {
  font-family: var(--font-heading);
  font-size: 1rem;
  margin-bottom: var(--space-md);
}

.order-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-sm) 0;
  border-bottom: 1px solid var(--color-border-light);
}

.order-item:last-child {
  border-bottom: none;
}

.order-item-name {
  font-weight: 500;
  font-size: 0.9rem;
}

.order-item-qty {
  display: block;
  font-size: 0.78rem;
  color: var(--color-text-light);
}

.order-item-price {
  font-weight: 600;
  font-size: 0.9rem;
}

.shipping-info {
  border-top: 1px solid var(--color-border-light);
}

.shipping-info p {
  font-size: 0.9rem;
  color: var(--color-text-muted);
  line-height: 1.5;
}

/* ─── Actions ─────────────────────────────────────────── */
.confirm-actions {
  display: flex;
  gap: var(--space-md);
  justify-content: center;
  margin-top: var(--space-2xl);
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
@media (max-width: 640px) {
  .details-header {
    grid-template-columns: 1fr 1fr;
  }
  .confirm-actions {
    flex-direction: column;
  }
}
</style>
