<script setup lang="ts">
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const handleLogout = () => {
  authStore.logout()
  router.push('/')
}
</script>

<template>
  <nav class="bg-white shadow-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between h-16">
        <div class="flex items-center">
          <router-link to="/" class="text-xl font-bold text-primary-600">
            Grand Hotel
          </router-link>
        </div>
        <div class="flex items-center space-x-4">
          <router-link
            to="/"
            class="text-secondary-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition"
          >
            Rooms
          </router-link>
          <template v-if="authStore.token">
            <router-link
              to="/admin/dashboard"
              class="text-secondary-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition"
            >
              Dashboard
            </router-link>
            <router-link
              to="/admin/reservations"
              class="text-secondary-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition"
            >
              Reservations
            </router-link>
            <button
              @click="handleLogout"
              class="bg-primary-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-primary-700 transition"
            >
              Logout
            </button>
          </template>
          <template v-else>
            <router-link
              to="/admin/login"
              class="text-secondary-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition"
            >
              Admin
            </router-link>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>