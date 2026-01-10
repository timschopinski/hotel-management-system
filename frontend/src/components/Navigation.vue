<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()
const mobileMenuOpen = ref(false)

const handleLogout = () => {
  authStore.logout()
  mobileMenuOpen.value = false
  router.push('/')
}

const closeMobileMenu = () => {
  mobileMenuOpen.value = false
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

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center space-x-4">
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

        <!-- Mobile menu button -->
        <div class="md:hidden flex items-center">
          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="text-secondary-700 hover:text-primary-600 p-2"
          >
            <svg
              class="h-6 w-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                v-if="!mobileMenuOpen"
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
              <path
                v-else
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Navigation -->
    <div v-if="mobileMenuOpen" class="md:hidden border-t border-secondary-200">
      <div class="px-2 pt-2 pb-3 space-y-1">
        <router-link
          to="/"
          @click="closeMobileMenu"
          class="block text-secondary-700 hover:text-primary-600 hover:bg-secondary-50 px-3 py-2 rounded-md text-base font-medium transition"
        >
          Rooms
        </router-link>
        <template v-if="authStore.token">
          <router-link
            to="/admin/dashboard"
            @click="closeMobileMenu"
            class="block text-secondary-700 hover:text-primary-600 hover:bg-secondary-50 px-3 py-2 rounded-md text-base font-medium transition"
          >
            Dashboard
          </router-link>
          <router-link
            to="/admin/reservations"
            @click="closeMobileMenu"
            class="block text-secondary-700 hover:text-primary-600 hover:bg-secondary-50 px-3 py-2 rounded-md text-base font-medium transition"
          >
            Reservations
          </router-link>
          <button
            @click="handleLogout"
            class="w-full text-left bg-primary-600 text-white px-3 py-2 rounded-md text-base font-medium hover:bg-primary-700 transition"
          >
            Logout
          </button>
        </template>
        <template v-else>
          <router-link
            to="/admin/login"
            @click="closeMobileMenu"
            class="block text-secondary-700 hover:text-primary-600 hover:bg-secondary-50 px-3 py-2 rounded-md text-base font-medium transition"
          >
            Admin
          </router-link>
        </template>
      </div>
    </div>
  </nav>
</template>