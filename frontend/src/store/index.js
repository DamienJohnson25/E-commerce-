import { defineStore } from 'pinia'

const API = '/api'

function getSessionId() {
  let id = localStorage.getItem('shopvue_session')
  if (!id) {
    id = 'session-' + Math.random().toString(36).substring(2, 15)
    localStorage.setItem('shopvue_session', id)
  }
  return id
}

export const useShopStore = defineStore('shop', {
  state: () => ({
    sessionId: getSessionId(),
    products: [],
    categories: [],
    cart: { items: [], total: 0, item_count: 0 },
    loading: false,
    error: null,
    searchQuery: '',
    selectedCategory: 'all',
    isAuthenticated: !!localStorage.getItem('isLoggedIn'),
    user: JSON.parse(localStorage.getItem('user')) || null,
    toast: null
  }),

  getters: {
    cartItemCount: (state) => state.cart.item_count || 0,
    cartTotal: (state) => state.cart.total || 0,
    isLoggedIn: (state) => state.isAuthenticated,
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

  actions: {
    showToast(message) {
      this.toast = message
      setTimeout(() => { this.toast = null }, 3000)
    },

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

    async login(credentials) {
      try {
        const res = await fetch(`${API}/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(credentials)
        })

        const data = await res.json()
        if (!res.ok) throw new Error(data.error || 'Login failed')

        this.isAuthenticated = true
        this.user = { name: data.name, email: data.email }

        localStorage.setItem('user', JSON.stringify(this.user))
        localStorage.setItem('isLoggedIn', 'true')

        return this.user
      } catch (err) {
        console.error('login error:', err)
        throw err
      }
    },

    async register(userData) {
      try {
        const res = await fetch(`${API}/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(userData)
        })

        const data = await res.json()
        if (!res.ok) throw new Error(data.error || 'Registration failed')

        this.isAuthenticated = true
        this.user = { name: data.name, email: data.email }

        localStorage.setItem('user', JSON.stringify(this.user))
        localStorage.setItem('isLoggedIn', 'true')

        return this.user
      } catch (err) {
        console.error('register error:', err)
        throw err
      }
    },

    logout() {
      this.isAuthenticated = false
      this.user = null
      localStorage.removeItem('user')
      localStorage.removeItem('isLoggedIn')
    },

    async deleteAccount() {
      try {
        if (!this.user) throw new Error('No logged-in user')

        const res = await fetch(`${API}/delete-account`, {
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: this.user.email })
        })

        // 🔍 DEBUG LOG (helps you see what's happening)
        console.log('DELETE response status:', res.status)

        const data = await res.json()

        if (!res.ok) throw new Error(data.error || 'Failed to delete account')

        this.logout()
        return data
      } catch (err) {
        console.error('deleteAccount error FULL:', err)
        throw err
      }
    }
  }
})
