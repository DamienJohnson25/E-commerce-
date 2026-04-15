import { describe, it, expect, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useShopStore } from './src/store/index.js'

describe('Shop Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
  })

  it('logs in a user', async () => {
    const store = useShopStore()

    await store.register({
      name: 'Test User',
      email: 'test@test.com',
      password: '1234'
    })

    const user = await store.login({
      email: 'test@test.com',
      password: '1234'
    })

    expect(store.isLoggedIn).toBe(true)
    expect(user.name).toBe('Test User')
  })

  it('adds item to cart', () => {
    const store = useShopStore()

    store.products = [{ id: 1, name: 'Item', price: 10 }]

    store.addToCart(1, 2)

    expect(store.cart.length).toBe(1)
    expect(store.cart[0].quantity).toBe(2)
  })

  it('persists cart in localStorage', () => {
    const store = useShopStore()

    store.products = [{ id: 1, name: 'Item', price: 10 }]
    store.addToCart(1, 1)

    const saved = JSON.parse(localStorage.getItem('cart'))

    expect(saved.length).toBe(1)
  })
})
