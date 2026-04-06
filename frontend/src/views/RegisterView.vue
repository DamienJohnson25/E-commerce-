<template>
  <div class="register-container">
    <h2>Create an Account</h2>

    <form @submit.prevent="registerUser">
      <!-- Name -->
      <div class="form-group">
        <label for="name">Full Name</label>
        <input type="text" id="name" v-model="form.name" />
        <small class="hint">Enter first and last name</small>
        <p v-if="errors.name" class="error">{{ errors.name }}</p>
      </div>

      <!-- Email -->
      <div class="form-group">
        <label for="email">Email</label>
        <input type="email" id="email" v-model="form.email" />
        <small class="hint">Enter a valid email address</small>
        <p v-if="errors.email" class="error">{{ errors.email }}</p>
      </div>

      <!-- Password -->
      <div class="form-group">
        <label for="password">Password</label>
        <input type="password" id="password" v-model="form.password" />
        <small class="hint">
          Must be 6+ characters, include 1 capital letter and 1 number
        </small>
        <p v-if="errors.password" class="error">{{ errors.password }}</p>
      </div>

      <button type="submit" class="btn btn-primary" :disabled="loading">
        {{ loading ? 'Registering...' : 'Register' }}
      </button>

      <p v-if="errors.general" class="error">{{ errors.general }}</p>
      <p v-if="successMessage" class="success">{{ successMessage }}</p>
    </form>

    <p class="switch">
      Already have an account?
      <span @click="goToLogin" class="link">Sign in</span>
    </p>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useShopStore } from '../store/index.js'

const router = useRouter()
const store = useShopStore()

const form = reactive({ name: '', email: '', password: '' })
const errors = reactive({ name: '', email: '', password: '', general: '' })
const successMessage = ref('')
const loading = ref(false)

function goToLogin() {
  router.push('/login')
}

function validateForm() {
  errors.name = ''
  errors.email = ''
  errors.password = ''
  errors.general = ''

  let valid = true
  const nameRegex = /^[A-Za-z]{2,}\s+[A-Za-z]{2,}$/
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  const passwordRegex = /^(?=.*[A-Z])(?=.*\d).{6,}$/

  if (!form.name.trim()) {
    errors.name = 'Please enter your full name'
    valid = false
  } else if (!nameRegex.test(form.name.trim())) {
    errors.name = 'Enter first and last name (e.g. John Smith)'
    valid = false
  }

  if (!form.email.trim()) {
    errors.email = 'Please enter your email'
    valid = false
  } else if (!emailRegex.test(form.email.trim())) {
    errors.email = 'Enter a valid email address'
    valid = false
  }

  if (!form.password) {
    errors.password = 'Please enter a password'
    valid = false
  } else if (!passwordRegex.test(form.password)) {
    errors.password =
      'Password must be 6+ chars, include 1 capital letter and 1 number'
    valid = false
  }

  return valid
}

async function registerUser() {
  if (!validateForm()) return

  loading.value = true
  successMessage.value = ''
  errors.general = ''

  try {
    const user = await store.register({
      name: form.name.trim(),
      email: form.email.trim(),
      password: form.password
    })

    const firstName = user?.name?.split(' ')[0] || 'User'
    successMessage.value = `Welcome to ShopVue, ${firstName}!`

    Object.assign(form, { name: '', email: '', password: '' })

    setTimeout(() => {
      router.push('/products')
    }, 800)
  } catch (err) {
    errors.general = err.message || 'Registration failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>


<style scoped>
.register-container {
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

