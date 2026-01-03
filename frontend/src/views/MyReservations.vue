<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../api'
import type { Reservation } from '../types'

const reservations = ref<Reservation[]>([])
const loading = ref(true)
const error = ref('')

const fetchReservations = async () => {
  try {
    const response = await api.get('/reservations/my')
    reservations.value = response.data
  } catch (err) {
    error.value = 'Failed to fetch reservations'
  } finally {
    loading.value = false
  }
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(() => {
  fetchReservations()
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <h1 class="text-3xl font-bold text-secondary-900 mb-8">
      My Reservations
    </h1>

    <div v-if="error" class="bg-red-50 border border-red-300 text-red-700 px-4 py-3 rounded mb-6">
      {{ error }}
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>

    <div v-else-if="reservations.length === 0" class="bg-white rounded-lg shadow-md p-8 text-center">
      <p class="text-secondary-600 text-lg">No reservations found</p>
    </div>

    <div v-else class="bg-white rounded-lg shadow-md overflow-hidden">
      <div class="overflow-x-auto">
        <table class="min-w-full divide-y divide-secondary-200">
          <thead class="bg-secondary-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-secondary-700 uppercase tracking-wider">
                Room
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-secondary-700 uppercase tracking-wider">
                Guest Name
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-secondary-700 uppercase tracking-wider">
                Guest Email
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-secondary-700 uppercase tracking-wider">
                Check-in
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-secondary-700 uppercase tracking-wider">
                Check-out
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-secondary-200">
            <tr v-for="reservation in reservations" :key="reservation.id" class="hover:bg-secondary-50">
              <td class="px-6 py-4 whitespace-nowrap text-sm font-medium text-secondary-900">
                {{ reservation.room?.name || 'N/A' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-secondary-700">
                {{ reservation.guest_name }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-secondary-700">
                {{ reservation.guest_email }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-secondary-700">
                {{ formatDate(reservation.start_date) }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-secondary-700">
                {{ formatDate(reservation.end_date) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>