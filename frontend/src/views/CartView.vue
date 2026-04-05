<!--
  CartView.vue — Shopping Cart Page
  ====================================
  Shows all items in the user's cart with quantity controls,
  subtotals, and a checkout button.

  Analogy: Looking at your tray before you go to the cashier.
-->

<template>
  <div class="container cart-page">
    <h1 class="page-title">Your Cart</h1>

    <!-- Empty Cart -->
    <div v-if="store.cart.items.length === 0" class="empty-state">
      <span class="empty-icon">🛒</span>
      <h3>Your cart is empty</h3>
      <p>Looks like you haven't added anything yet.</p>
      <router-link to="/products" class="btn btn-primary">Start Shopping</router-link>
    </div>

    <!-- Cart Items -->
    <div v-else class="cart-layout">
      <div class="cart-items">
        <div v-for="item in store.cart.items" :key="item.id" class="cart-item card">
          <!-- Item Image -->
          <router-link :to="`/product/${item.product_id}`" class="cart-item-image-wrap">
            <img :src="item.image_url" :alt="item.name" class="cart-item-image" />
          </router-link>

          <!-- Item Details -->
          <div class="cart-item-info">
            <router-link :to="`/product/${item.product_id}`" class="cart-item-name">
              {{ item.name }}
            </router-link>
            <p class="cart-item-price">${{ item.price.toFixed(2) }}</p>

            <!-- Quantity Controls -->
            <div class="cart-item-actions">
              <div class="qty-selector">
                <button class="qty-btn" @click="updateQty(item, -1)">−</button>
                <span class="qty-value">{{ item.quantity }}</span>
                <button class="qty-btn" @click="updateQty(item, 1)">+</button>
              </div>
              <button class="btn btn-ghost remove-btn" @click="store.removeFromCart(item.id)">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 01-2 2H7a2 2 0 01-2-2V6m3 0V4a2 2 0 012-2h4a2 2 0 012 2v2"/>
                </svg>
                Remove
              </button>
            </div>
          </div>

          <!-- Line Total -->
          <div class="cart-item-total">
            ${{ (item.price * item.quantity).toFixed(2) }}
          </div>
        </div>
      </div>

      <!-- Order Summary Sidebar -->
      <div class="cart-summary card">
        <h3 class="summary-title">Order Summary</h3>

        <div class="summary-lines">
          <div class="summary-line">
            <span>Subtotal ({{ store.cartItemCount }} items)</span>
            <span>${{ store.cartTotal.toFixed(2) }}</span>
          </div>
          <div class="summary-line">
            <span>Shipping</span>
            <span class="free-shipping">Free</span>
          </div>
          <div class="summary-line">
            <span>Tax (estimated)</span>
            <span>${{ (store.cartTotal * 0.08).toFixed(2) }}</span>
          </div>
        </div>

        <div class="summary-total">
          <span>Total</span>
          <span>${{ (store.cartTotal * 1.08).toFixed(2) }}</span>
        </div>

        <router-link to="/checkout" class="btn btn-primary btn-lg summary-checkout">
          Proceed to Checkout
        </router-link>

        <router-link to="/products" class="continue-link">
          ← Continue Shopping
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useShopStore } from '../store/index.js'

const store = useShopStore()

function updateQty(item, delta) {
  const newQty = item.quantity + delta
  if (newQty <= 0) {
    store.removeFromCart(item.id)
  } else {
    store.updateCartItem(item.id, newQty)
  }
}
</script>

<style scoped>
.cart-page {
  padding-top: var(--space-lg);
}

.page-title {
  font-family: var(--font-heading);
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: var(--space-xl);
}

/* ─── Layout ──────────────────────────────────────────── */
.cart-layout {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: var(--space-xl);
  align-items: start;
}

/* ─── Cart Items ──────────────────────────────────────── */
.cart-items {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}

.cart-item {
  display: flex;
  align-items: center;
  gap: var(--space-lg);
  padding: var(--space-lg);
}

.cart-item-image-wrap {
  flex-shrink: 0;
  width: 100px;
  height: 100px;
  border-radius: var(--radius-md);
  overflow: hidden;
  background: var(--color-border-light);
}

.cart-item-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cart-item-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}

.cart-item-name {
  font-weight: 600;
  font-size: 1rem;
  color: var(--color-text);
  transition: color 0.2s;
}

.cart-item-name:hover {
  color: var(--color-accent);
}

.cart-item-price {
  font-size: 0.9rem;
  color: var(--color-text-muted);
}

.cart-item-actions {
  display: flex;
  align-items: center;
  gap: var(--space-md);
  margin-top: var(--space-xs);
}

.qty-selector {
  display: flex;
  align-items: center;
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-sm);
  overflow: hidden;
}

.qty-btn {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  color: var(--color-text);
  transition: background 0.15s;
}

.qty-btn:hover {
  background: var(--color-border-light);
}

.qty-value {
  width: 32px;
  text-align: center;
  font-weight: 600;
  font-size: 0.85rem;
}

.remove-btn {
  font-size: 0.8rem;
  color: var(--color-text-light);
  display: flex;
  align-items: center;
  gap: 4px;
}

.remove-btn:hover {
  color: var(--color-danger);
}

.cart-item-total {
  font-size: 1.05rem;
  font-weight: 700;
  white-space: nowrap;
}

/* ─── Summary Sidebar ─────────────────────────────────── */
.cart-summary {
  padding: var(--space-xl);
  position: sticky;
  top: 80px;
}

.summary-title {
  font-family: var(--font-heading);
  font-size: 1.15rem;
  margin-bottom: var(--space-lg);
}

.summary-lines {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
  padding-bottom: var(--space-lg);
  border-bottom: 1px solid var(--color-border-light);
}

.summary-line {
  display: flex;
  justify-content: space-between;
  font-size: 0.9rem;
  color: var(--color-text-muted);
}

.free-shipping {
  color: var(--color-success);
  font-weight: 500;
}

.summary-total {
  display: flex;
  justify-content: space-between;
  font-size: 1.1rem;
  font-weight: 700;
  padding: var(--space-lg) 0;
}

.summary-checkout {
  width: 100%;
  text-align: center;
}

.continue-link {
  display: block;
  text-align: center;
  font-size: 0.85rem;
  color: var(--color-text-muted);
  margin-top: var(--space-md);
  transition: color 0.2s;
}

.continue-link:hover {
  color: var(--color-accent);
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
  font-size: 1.3rem;
}

/* ─── Responsive ──────────────────────────────────────── */
@media (max-width: 768px) {
  .cart-layout {
    grid-template-columns: 1fr;
  }
  .cart-item {
    flex-wrap: wrap;
  }
  .cart-item-total {
    width: 100%;
    text-align: right;
    padding-top: var(--space-sm);
    border-top: 1px solid var(--color-border-light);
  }
}
</style>
