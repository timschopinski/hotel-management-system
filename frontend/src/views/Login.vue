<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const handleLogin = async () => {
  error.value = ''
  loading.value = true

  try {
    await authStore.login({ email: email.value, password: password.value })
    router.push('/admin/dashboard')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="max-w-md mx-auto px-4 py-12">
    <div class="bg-white rounded-lg shadow-md p-8">
      <h1 class="text-3xl font-bold text-secondary-900 mb-6 text-center">
        Admin Login
      </h1>

      <form @submit.prevent="handleLogin" class="space-y-6">
        <div>
          <label for="email" class="block text-sm font-medium text-secondary-700 mb-2">
            Email
          </label>
          <input
            id="email"
            v-model="email"
            type="email"
            required
            class="w-full px-3 py-2 border border-secondary-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        <div>
          <label for="password" class="block text-sm font-medium text-secondary-700 mb-2">
            Password
          </label>
          <input
            id="password"
            v-model="password"
            type="password"
            required
            class="w-full px-3 py-2 border border-secondary-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        <div v-if="error" class="bg-red-50 border border-red-300 text-red-700 px-4 py-3 rounded">
          {{ error }}
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full bg-primary-600 text-white py-2 rounded-md hover:bg-primary-700 transition disabled:opacity-50"
        >
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>

      <p class="mt-6 text-center text-secondary-600">
        Don't have an account?
        <router-link to="/admin/register" class="text-primary-600 hover:text-primary-700 font-medium">
          Register
        </router-link>
      </p>
    </div>
  </div>
</template>