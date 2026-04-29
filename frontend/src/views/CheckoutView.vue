<!--
  CheckoutView.vue — Checkout Form
  ====================================
  Collects shipping info and places the order.
  Analogy: Filling out the "pay here" slip at the register.
-->

<template>
  <div class="container checkout-page">
    <h1 class="page-title">Checkout</h1>

    <!-- Redirect if cart is empty -->
    <div v-if="store.cart.items.length === 0 && !submitting" class="empty-state">
      <span class="empty-icon">📦</span>
      <h3>Nothing to check out</h3>
      <p>Add some items to your cart first.</p>
      <router-link to="/products" class="btn btn-primary">Browse Products</router-link>
    </div>

    <div v-else class="checkout-layout">
      <!-- Shipping Form -->
      <div class="checkout-form card">
        <h2 class="form-section-title">Shipping Information</h2>

        <div class="form-grid">
          <div class="form-group">
            <label class="form-label">Full Name</label>
            <input
              v-model="form.customer_name"
              class="form-input"
              type="text"
              placeholder="Jane Doe"
              :class="{ error: errors.customer_name }"
            />
            <span v-if="errors.customer_name" class="form-error">{{ errors.customer_name }}</span>
          </div>

          <div class="form-group">
            <label class="form-label">Email Address</label>
            <input
              v-model="form.customer_email"
              class="form-input"
              type="email"
              placeholder="jane@example.com"
              :class="{ error: errors.customer_email }"
            />
            <span v-if="errors.customer_email" class="form-error">{{ errors.customer_email }}</span>
          </div>

          <div class="form-group full-width">
            <label class="form-label">Street Address</label>
            <input
              v-model="form.address"
              class="form-input"
              type="text"
              placeholder="123 Main Street, Apt 4B"
              :class="{ error: errors.address }"
            />
            <span v-if="errors.address" class="form-error">{{ errors.address }}</span>
          </div>

          <div class="form-group">
            <label class="form-label">City</label>
            <input
              v-model="form.city"
              class="form-input"
              type="text"
              placeholder="Portland"
              :class="{ error: errors.city }"
            />
            <span v-if="errors.city" class="form-error">{{ errors.city }}</span>
          </div>

          <div class="form-group">
            <label class="form-label">ZIP Code</label>
            <input
              v-model="form.zip_code"
              class="form-input"
              type="text"
              placeholder="97201"
              :class="{ error: errors.zip_code }"
            />
            <span v-if="errors.zip_code" class="form-error">{{ errors.zip_code }}</span>
          </div>
        </div>

        <button
          class="btn btn-primary btn-lg place-order-btn"
          @click="handlePlaceOrder"
          :disabled="submitting"
        >
          {{ submitting ? 'Placing Order...' : 'Place Order' }}
        </button>
      </div>

      <!-- Order Review Sidebar -->
      <div class="order-review card">
        <h3 class="review-title">Order Review</h3>

        <div class="review-items">
          <div v-for="item in store.cart.items" :key="item.id" class="review-item">
            <img :src="item.image_url" :alt="item.name" class="review-thumb" />
            <div class="review-item-info">
              <p class="review-item-name">{{ item.name }}</p>
              <p class="review-item-qty">Qty: {{ item.quantity }}</p>
            </div>
            <span class="review-item-price">${{ (item.price * item.quantity).toFixed(2) }}</span>
          </div>
        </div>

        <div class="review-totals">
          <div class="review-line">
            <span>Subtotal</span>
            <span>${{ store.cartTotal.toFixed(2) }}</span>
          </div>
          <div class="review-line">
            <span>Shipping</span>
            <span class="free">Free</span>
          </div>
          <div class="review-line">
            <span>Tax</span>
            <span>${{ (store.cartTotal * 0.08).toFixed(2) }}</span>
          </div>
          <div class="review-line total">
            <span>Total</span>
            <span>${{ (store.cartTotal * 1.08).toFixed(2) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useShopStore } from '../store/index.js'

const store = useShopStore()
const router = useRouter()
const submitting = ref(false)

// Stripe publishable key placeholder.
// Replace this value in frontend/.env or Vite env variables.
const stripePublishableKey = import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY || 'pk_test_YOUR_PUBLISHABLE_KEY_HERE'

const form = reactive({
  customer_name: '',
  customer_email: '',
  address: '',
  city: '',
  zip_code: ''
})

const errors = reactive({
  customer_name: '',
  customer_email: '',
  address: '',
  city: '',
  zip_code: ''
})

function validate() {
  let valid = true
  // Reset errors
  Object.keys(errors).forEach(k => errors[k] = '')

  if (!form.customer_name.trim()) {
    errors.customer_name = 'Name is required'
    valid = false
  }
  if (!form.customer_email.trim()) {
    errors.customer_email = 'Email is required'
    valid = false
  } else if (!/\S+@\S+\.\S+/.test(form.customer_email)) {
    errors.customer_email = 'Enter a valid email'
    valid = false
  }
  if (!form.address.trim()) {
    errors.address = 'Address is required'
    valid = false
  }
  if (!form.city.trim()) {
    errors.city = 'City is required'
    valid = false
  }
  if (!form.zip_code.trim()) {
    errors.zip_code = 'ZIP code is required'
    valid = false
  }
  return valid
}

async function handlePlaceOrder() {
  if (!validate()) return

  submitting.value = true
  try {
    const session = await store.createCheckoutSession({
      ...form,
      stripe_publishable_key: stripePublishableKey
    })
    window.location.href = session.url
  } catch (err) {
    // Error is handled by the store's showToast
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.checkout-page {
  padding-top: var(--space-lg);
}

.page-title {
  font-family: var(--font-heading);
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: var(--space-xl);
}

.checkout-layout {
  display: grid;
  grid-template-columns: 1fr 380px;
  gap: var(--space-xl);
  align-items: start;
}

/* ─── Form ────────────────────────────────────────────── */
.checkout-form {
  padding: var(--space-xl);
}

.form-section-title {
  font-family: var(--font-heading);
  font-size: 1.2rem;
  margin-bottom: var(--space-xl);
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-lg);
}

.full-width {
  grid-column: 1 / -1;
}

.form-input.error {
  border-color: var(--color-danger);
}

.form-error {
  font-size: 0.78rem;
  color: var(--color-danger);
  margin-top: 2px;
}

.place-order-btn {
  width: 100%;
  margin-top: var(--space-xl);
}

/* ─── Order Review ────────────────────────────────────── */
.order-review {
  padding: var(--space-xl);
  position: sticky;
  top: 80px;
}

.review-title {
  font-family: var(--font-heading);
  font-size: 1.1rem;
  margin-bottom: var(--space-lg);
}

.review-items {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
  padding-bottom: var(--space-lg);
  border-bottom: 1px solid var(--color-border-light);
}

.review-item {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.review-thumb {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-sm);
  object-fit: cover;
  background: var(--color-border-light);
}

.review-item-info {
  flex: 1;
}

.review-item-name {
  font-size: 0.85rem;
  font-weight: 500;
}

.review-item-qty {
  font-size: 0.78rem;
  color: var(--color-text-light);
}

.review-item-price {
  font-size: 0.9rem;
  font-weight: 600;
}

.review-totals {
  padding-top: var(--space-lg);
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.review-line {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: var(--color-text-muted);
}

.review-line.total {
  padding-top: var(--space-md);
  border-top: 1px solid var(--color-border-light);
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--color-text);
}

.free {
  color: var(--color-success);
  font-weight: 500;
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

.empty-icon { font-size: 3rem; }

.empty-state h3 {
  font-family: var(--font-heading);
  color: var(--color-text);
}

/* ─── Responsive ──────────────────────────────────────── */
@media (max-width: 768px) {
  .checkout-layout {
    grid-template-columns: 1fr;
  }
  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>
