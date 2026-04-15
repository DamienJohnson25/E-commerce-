<template>
  <div class="container success-page">
    <h1>✅ Payment Successful</h1>
    <p>Thank you for your purchase!</p>

    <router-link to="/products" class="btn btn-primary">
      Continue Shopping
    </router-link>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useShopStore } from '../store/index.js'

const store = useShopStore()

onMounted(() => {
  store.clearCart()
})
</script>

<style scoped>
.success-page {
  text-align: center;
  padding: 3rem;
}
</style>
