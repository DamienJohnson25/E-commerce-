/**
 * store/index.js — State Management (Pinia)
 * ============================================
 * The store is a SHARED WHITEBOARD that all components can
 * read from and write to. It holds:
 * - The product catalog
 * - The shopping cart
 * - The session ID (to track this user's cart)
 *
 * Analogy: In a restaurant kitchen, there's a ticket board
 * where all chefs can see every order. That's our store.
 */

import { defineStore } from 'pinia'

// Base URL for API calls — uses Vite's proxy in development
const API = '/api'

/**
 * Generate a unique session ID for this browser tab.
 * In a real app, this would come from authentication.
 * For now, we store it in localStorage so it survives page refreshes.
 */
function getSessionId() {
  let id = localStorage.getItem('shopvue_session')
  if (!id) {
    id = 'session-' + Math.random().toString(36).substring(2, 15)
    localStorage.setItem('shopvue_session', id)
  }
  return id
}

// ─── Main Store ──────────────────────────────────────────────────

export const useShopStore = defineStore('shop', {
  /**
   * STATE — The data our app "remembers"
   * Like the current contents of the kitchen whiteboard
   */
  state: () => ({
    sessionId: getSessionId(),
    products: [],
    categories: [],
    cart: { items: [], total: 0, item_count: 0 },
    loading: false,
    error: null,
    searchQuery: '',
    selectedCategory: 'all',
    toast: null
  }),

  /**
   * GETTERS — Computed values derived from state
   * Like asking "how many orders are pending?" by counting tickets
   */
  getters: {
    cartItemCount: (state) => state.cart.item_count || 0,
    cartTotal: (state) => state.cart.total || 0,
    featuredProducts: (state) => state.products.filter(p => p.featured),
    filteredProducts: (state) => {
      let result = state.products
      if (state.selectedCategory && state.selectedCategory !== 'all') {
        result = result.filter(p => p.category === state.selectedCategory)
      }
      if (state.searchQuery) {
        const q = state.searchQuery.toLowerCase()
        result = result.filter(p =>
          p.name.toLowerCase().includes(q) ||
          p.description.toLowerCase().includes(q)
        )
      }
      return result
    }
  },

  /**
   * ACTIONS — Functions that fetch data or modify state
   * Like the chef's instructions: "Go fetch ingredients" or "Update the ticket"
   */
  actions: {
    // ── Show a toast notification ──
    showToast(message) {
      this.toast = message
      setTimeout(() => { this.toast = null }, 3000)
    },

    // ── Fetch all products from the backend ──
    async fetchProducts() {
      this.loading = true
      this.error = null
      try {
        const res = await fetch(`${API}/products`)
        if (!res.ok) throw new Error('Failed to fetch products')
        this.products = await res.json()
      } catch (err) {
        this.error = err.message
        console.error('fetchProducts error:', err)
      } finally {
        this.loading = false
      }
    },

    // ── Fetch categories ──
    async fetchCategories() {
      try {
        const res = await fetch(`${API}/categories`)
        this.categories = await res.json()
      } catch (err) {
        console.error('fetchCategories error:', err)
      }
    },

    // ── Search products ──
    async searchProducts(query) {
      this.searchQuery = query
      if (!query.trim()) {
        await this.fetchProducts()
        return
      }
      this.loading = true
      try {
        const res = await fetch(`${API}/products/search?q=${encodeURIComponent(query)}`)
        this.products = await res.json()
      } catch (err) {
        this.error = err.message
      } finally {
        this.loading = false
      }
    },

    // ── Fetch the current cart from the backend ──
    async fetchCart() {
      try {
        const res = await fetch(`${API}/cart/${this.sessionId}`)
        this.cart = await res.json()
      } catch (err) {
        console.error('fetchCart error:', err)
      }
    },

    // ── Add an item to the cart ──
    async addToCart(productId, quantity = 1) {
      try {
        const res = await fetch(`${API}/cart`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            session_id: this.sessionId,
            product_id: productId,
            quantity
          })
        })
        if (!res.ok) {
          const err = await res.json()
          throw new Error(err.error)
        }
        await this.fetchCart()
        this.showToast('Added to cart!')
      } catch (err) {
        this.showToast(err.message)
      }
    },

    // ── Update cart item quantity ──
    async updateCartItem(itemId, quantity) {
      try {
        await fetch(`${API}/cart/${itemId}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ quantity })
        })
        await this.fetchCart()
      } catch (err) {
        console.error('updateCartItem error:', err)
      }
    },

    // ── Remove an item from the cart ──
    async removeFromCart(itemId) {
      try {
        await fetch(`${API}/cart/${itemId}`, { method: 'DELETE' })
        await this.fetchCart()
        this.showToast('Item removed')
      } catch (err) {
        console.error('removeFromCart error:', err)
      }
    },

    // ── Place an order ──
    async placeOrder(customerInfo) {
      try {
        const res = await fetch(`${API}/orders`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            session_id: this.sessionId,
            ...customerInfo
          })
        })
        if (!res.ok) {
          const err = await res.json()
          throw new Error(err.error)
        }
        const order = await res.json()
        this.cart = { items: [], total: 0, item_count: 0 }
        return order
      } catch (err) {
        this.showToast(err.message)
        throw err
      }
    }
  }
})
