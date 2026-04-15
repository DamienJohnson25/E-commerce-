import { defineStore } from 'pinia'

export const useShopStore = defineStore('shop', {
  state: () => ({
    cart: [],
    products: [],
    isLoggedIn: false,
    user: null,

    searchQuery: '',
    selectedCategory: '',
    minPrice: '',
    maxPrice: ''
  }),

  getters: {
    cartItemCount: (state) =>
      state.cart.reduce((sum, item) => sum + item.quantity, 0),

    cartTotal: (state) =>
      state.cart.reduce((sum, item) => sum + item.price * item.quantity, 0),

    featuredProducts: (state) =>
      (state.products || []).map(product => ({
        ...product,
        id: product.id || product._id || '',
        featured: Boolean(product.featured),
        image: product.image_url || '',
      }))
  },

  actions: {
    async fetchProducts() {
      try {
        const res = await fetch('/api/products')
        const data = await res.json()
        this.products = data
      } catch (err) {
        console.error(err)
        this.products = []
      }
    },

    async searchProducts() {
      try {
        const params = new URLSearchParams()

        if (this.searchQuery) params.append('q', this.searchQuery)
        if (this.selectedCategory) params.append('category', this.selectedCategory)
        if (this.minPrice) params.append('min_price', this.minPrice)
        if (this.maxPrice) params.append('max_price', this.maxPrice)

        const res = await fetch(`/api/products/search?${params.toString()}`)
        const data = await res.json()

        this.products = data
      } catch (err) {
        console.error('search error:', err)
      }
    },

    addToCart(productId, quantity = 1) {
      const existing = this.cart.find(item => item.id === productId)

      if (existing) {
        existing.quantity += quantity
      } else {
        const product =
          this.products.find(p => p.id === productId) || {
            id: productId,
            price: 0,
            name: ''
          }

        this.cart.push({ ...product, quantity })
      }

      this.saveCart()
    },

    updateCartItem(productId, quantity) {
      const item = this.cart.find(i => i.id === productId)

      if (item) {
        item.quantity = quantity
        this.saveCart()
      }
    },

    removeFromCart(productId) {
      this.cart = this.cart.filter(item => item.id !== productId)
      this.saveCart()
    },

    clearCart() {
      this.cart = []
      localStorage.removeItem('cart')
    },

    login({ email, password }) {
      return fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      })
        .then(res => res.json().then(data => ({ res, data })))
        .then(({ res, data }) => {
          if (!res.ok) throw new Error(data.error)

          this.isLoggedIn = true
          this.user = data

          localStorage.setItem('user', JSON.stringify(data))
          localStorage.setItem('isLoggedIn', 'true')

          return data
        })
    },

    register({ name, email, password }) {
      return fetch('/api/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, email, password })
      })
        .then(res => res.json().then(data => ({ res, data })))
        .then(({ res, data }) => {
          if (!res.ok) throw new Error(data.error)

          this.isLoggedIn = true
          this.user = data

          localStorage.setItem('user', JSON.stringify(data))
          localStorage.setItem('isLoggedIn', 'true')

          return data
        })
    },

    async deleteAccount() {
      if (!this.user?.id) throw new Error('No user logged in')

      const res = await fetch(`/api/user/${this.user.id}`, {
        method: 'DELETE'
      })

      const data = await res.json()

      if (!res.ok) throw new Error(data.error)

      this.user = null
      this.isLoggedIn = false

      localStorage.removeItem('user')
      localStorage.removeItem('isLoggedIn')
    },

    logout() {
      this.isLoggedIn = false
      this.user = null
      this.clearCart()

      localStorage.removeItem('isLoggedIn')
      localStorage.removeItem('user')
    },

    initAuth() {
      this.isLoggedIn = localStorage.getItem('isLoggedIn') === 'true'
      const savedUser = localStorage.getItem('user')
      this.user = savedUser ? JSON.parse(savedUser) : null
    },

    initCart() {
      const savedCart = localStorage.getItem('cart')

      try {
        this.cart = savedCart ? JSON.parse(savedCart) : []
      } catch (e) {
        console.error('Cart parse error:', e)
        this.cart = []
      }

      // force Vue reactivity refresh
      this.cart = [...this.cart]
    },

    setProducts(productsArray) {
      this.products = productsArray
    },

    // 🔥 NEW: safe full store init (VERY IMPORTANT)
    initStore() {
      this.initCart()
      this.initAuth()
    },

    saveCart() {
      localStorage.setItem('cart', JSON.stringify(this.cart))
    }
  }
})
