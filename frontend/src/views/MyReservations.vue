<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import api from '../api'
import type { Reservation, Room } from '../types'

const reservations = ref<Reservation[]>([])
const myRooms = ref<Room[]>([])
const loading = ref(true)
const error = ref('')

const filterRoomId = ref<number | null>(null)
const filterGuestName = ref('')
const filterStartDate = ref('')
const filterEndDate = ref('')
const sortBy = ref('created_at')
const sortOrder = ref('desc')

const editingReservation = ref<Reservation | null>(null)
const editNotes = ref('')

const fetchReservations = async () => {
  try {
    const params = new URLSearchParams()
    if (filterRoomId.value) params.append('room_id', filterRoomId.value.toString())
    if (filterGuestName.value) params.append('guest_name', filterGuestName.value)
    if (filterStartDate.value) params.append('start_date', filterStartDate.value)
    if (filterEndDate.value) params.append('end_date', filterEndDate.value)
    params.append('sort_by', sortBy.value)
    params.append('sort_order', sortOrder.value)

    const response = await api.get(`/reservations/my?${params.toString()}`)
    reservations.value = response.data
  } catch (err) {
    error.value = 'Failed to fetch reservations'
  } finally {
    loading.value = false
  }
}

const fetchMyRooms = async () => {
  try {
    const response = await api.get('/rooms/my')
    myRooms.value = response.data
  } catch (err) {
    console.error('Failed to fetch rooms')
  }
}

const applyFilters = () => {
  loading.value = true
  fetchReservations()
}

const clearFilters = () => {
  filterRoomId.value = null
  filterGuestName.value = ''
  filterStartDate.value = ''
  filterEndDate.value = ''
  sortBy.value = 'created_at'
  sortOrder.value = 'desc'
  applyFilters()
}

const startEditNotes = (reservation: Reservation) => {
  editingReservation.value = reservation
  editNotes.value = reservation.notes || ''
}

const saveNotes = async () => {
  if (!editingReservation.value) return

  try {
    await api.patch(`/reservations/${editingReservation.value.id}`, {
      notes: editNotes.value || null
    })
    editingReservation.value = null
    await fetchReservations()
  } catch (err) {
    error.value = 'Failed to update notes'
  }
}

const cancelEdit = () => {
  editingReservation.value = null
  editNotes.value = ''
}

const formatDate = (dateString: string) => {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

onMounted(() => {
  fetchMyRooms()
  fetchReservations()
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <h1 class="text-3xl font-bold text-secondary-900 mb-8">
      Reservations Management
    </h1>

    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 class="text-xl font-semibold text-secondary-900 mb-4">
        Filters
      </h2>
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-4">
        <div>
          <label class="block text-sm font-medium text-secondary-700 mb-2">
            Room
          </label>
          <select
            v-model="filterRoomId"
            class="w-full px-3 py-2 border border-secondary-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option :value="null">All Rooms</option>
            <option v-for="room in myRooms" :key="room.id" :value="room.id">
              {{ room.name }}
            </option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-secondary-700 mb-2">
            Guest Name
          </label>
          <input
            v-model="filterGuestName"
            type="text"
            placeholder="Search by guest name"
            class="w-full px-3 py-2 border border-secondary-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-secondary-700 mb-2">
            Start Date (From)
          </label>
          <input
            v-model="filterStartDate"
            type="date"
            class="w-full px-3 py-2 border border-secondary-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-secondary-700 mb-2">
            End Date (To)
          </label>
          <input
            v-model="filterEndDate"
            type="date"
            class="w-full px-3 py-2 border border-secondary-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-secondary-700 mb-2">
            Sort By
          </label>
          <select
            v-model="sortBy"
            class="w-full px-3 py-2 border border-secondary-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="created_at">Created Date</option>
            <option value="start_date">Check-in Date</option>
            <option value="end_date">Check-out Date</option>
            <option value="guest_name">Guest Name</option>
          </select>
        </div>

        <div>
          <label class="block text-sm font-medium text-secondary-700 mb-2">
            Sort Order
          </label>
          <select
            v-model="sortOrder"
            class="w-full px-3 py-2 border border-secondary-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          >
            <option value="desc">Descending</option>
            <option value="asc">Ascending</option>
          </select>
        </div>
      </div>

      <div class="flex gap-4">
        <button
          @click="applyFilters"
          class="bg-primary-600 text-white px-6 py-2 rounded-md hover:bg-primary-700 transition"
        >
          Apply Filters
        </button>
        <button
          @click="clearFilters"
          class="bg-secondary-600 text-white px-6 py-2 rounded-md hover:bg-secondary-700 transition"
        >
          Clear Filters
        </button>
      </div>
    </div>

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
              <th class="px-6 py-3 text-left text-xs font-medium text-secondary-700 uppercase tracking-wider">
                Notes
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-secondary-700 uppercase tracking-wider">
                Actions
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
              <td class="px-6 py-4 text-sm text-secondary-700">
                <template v-if="editingReservation?.id === reservation.id">
                  <textarea
                    v-model="editNotes"
                    rows="2"
                    class="w-full px-2 py-1 border border-secondary-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 text-sm"
                  ></textarea>
                </template>
                <template v-else>
                  <div class="max-w-xs truncate" :title="reservation.notes || 'No notes'">
                    {{ reservation.notes || 'No notes' }}
                  </div>
                </template>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm">
                <template v-if="editingReservation?.id === reservation.id">
                  <div class="flex gap-2">
                    <button
                      @click="saveNotes"
                      class="text-green-600 hover:text-green-900"
                    >
                      Save
                    </button>
                    <button
                      @click="cancelEdit"
                      class="text-secondary-600 hover:text-secondary-900"
                    >
                      Cancel
                    </button>
                  </div>
                </template>
                <template v-else>
                  <button
                    @click="startEditNotes(reservation)"
                    class="text-primary-600 hover:text-primary-900"
                  >
                    Edit Notes
                  </button>
                </template>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>