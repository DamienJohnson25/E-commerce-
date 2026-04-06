<template>
  <div class="account-container">
    <h2>My Account</h2>

    <div v-if="store.user" class="account-card">
      <p><strong>Name:</strong> {{ store.user.name }}</p>
      <p><strong>Email:</strong> {{ store.user.email }}</p>

      <div class="actions">
        <button class="btn btn-logout" @click="logout">
          Log Out
        </button>

        <button class="btn btn-danger" @click="deleteAccount">
          Delete My Account
        </button>
      </div>
    </div>

    <p v-else>Loading account...</p>
  </div>
</template>

<script setup>
import { useShopStore } from '../store/index.js'
import { useRouter } from 'vue-router'

const store = useShopStore()
const router = useRouter()

function logout() {
  store.logout()
  router.push('/login')
}

async function deleteAccount() {
  const confirmDelete = confirm(
    'Are you sure you want to permanently delete your account? This cannot be undone.'
  )
  if (!confirmDelete) return

  try {
    await store.deleteAccount()
    alert('Your account has been deleted.')
    router.push('/')
  } catch (err) {
    alert(err.message || 'Failed to delete account.')
  }
}
</script>

<style scoped>
.account-container {
  max-width: 500px;
  margin: 3rem auto;
  padding: 2rem;
}
.account-card {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 1.5rem;
  background: var(--color-surface);
  box-shadow: var(--shadow-sm);
}
h2 {
  text-align: center;
  margin-bottom: 1.5rem;
}
.actions {
  margin-top: 1.5rem;
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}
.btn {
  flex: 1;
  padding: 0.7rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
}
.btn-logout {
  background: #ccc;
}
.btn-danger {
  background: red;
  color: white;
}
</style>
