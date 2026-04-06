<template>
  <div class="login-container">
    <h2>Sign In</h2>

    <form @submit.prevent="loginUser">
      <!-- Email -->
      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" v-model="form.email" />
        <small class="hint">Enter your registered email</small>
        <p v-if="errors.email" class="error">{{ errors.email }}</p>
      </div>

      <!-- Password -->
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="form.password" />
        <small class="hint">Enter your password</small>
        <p v-if="errors.password" class="error">{{ errors.password }}</p>
      </div>

      <button type="submit" class="btn btn-primary" :disabled="loading">
        {{ loading ? 'Signing in...' : 'Sign In' }}
      </button>

      <p v-if="loginError" class="error">{{ loginError }}</p>
      <p v-if="successMessage" class="success">{{ successMessage }}</p>
    </form>

    <p class="switch">
      Don't have an account?
      <span @click="goToRegister" class="link">Create one</span>
    </p>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useShopStore } from '../store/index.js'

const router = useRouter()
const store = useShopStore()

const form = reactive({ email: '', password: '' })
const errors = reactive({ email: '', password: '' })
const loginError = ref('')
const successMessage = ref('')
const loading = ref(false)

function goToRegister() {
  router.push('/register')
}

function validateForm() {
  errors.email = ''
  errors.password = ''
  loginError.value = ''

  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

  if (!form.email.trim()) errors.email = 'Please enter your email'
  else if (!emailRegex.test(form.email.trim()))
    errors.email = 'Enter a valid email address'

  if (!form.password) errors.password = 'Please enter your password'

  return !errors.email && !errors.password
}

async function loginUser() {
  if (!validateForm()) return

  loading.value = true
  loginError.value = ''
  successMessage.value = ''

  try {
    const user = await store.login({
      email: form.email.trim(),
      password: form.password
    })

    const firstName = user?.name?.split(' ')[0] || 'User'
    successMessage.value = `Welcome back, ${firstName}!`

    setTimeout(() => router.push('/products'), 800)
  } catch (err) {
    loginError.value = err.message || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>


<style scoped>
.login-container {
  max-width: 400px;
  margin: 3rem auto;
  padding: 2rem;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-sm);
  background: var(--color-surface);
}

h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: var(--color-text);
}

.form-group {
  margin-bottom: 1.2rem;
}

label {
  display: block;
  margin-bottom: 0.4rem;
  font-weight: 600;
  color: var(--color-text-muted);
}

input {
  width: 100%;
  padding: 0.75rem 1rem;
  border-radius: var(--radius-md);
  border: 1.5px solid var(--color-border);
  font-size: 1rem;
  background: var(--color-surface);
  color: var(--color-text);
}

input:focus {
  border-color: var(--color-accent);
  outline: none;
  box-shadow: 0 0 0 3px var(--color-accent-light);
}

.error {
  color: var(--color-danger);
  font-size: 0.85rem;
  margin-top: 4px;
  text-align: center;
}

.success {
  margin-top: 1rem;
  color: var(--color-success);
  font-weight: 600;
  text-align: center;
}

.hint {
  display: block;
  font-size: 0.75rem;
  color: var(--color-text-light);
  margin-top: 2px;
}

.switch {
  text-align: center;
  margin-top: 1rem;
}

.link {
  color: var(--color-accent);
  cursor: pointer;
  font-weight: 600;
}

button:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}
</style>
