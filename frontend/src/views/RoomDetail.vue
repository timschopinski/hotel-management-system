<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import api from '../api'
import type { Room, Reservation, CreateReservation } from '../types'

const route = useRoute()
const room = ref<Room | null>(null)
const reservations = ref<Reservation[]>([])
const loading = ref(true)
const error = ref('')

const guestName = ref('')
const guestEmail = ref('')
const notes = ref('')
const startDate = ref('')
const endDate = ref('')
const selectedDates = ref<string[]>([])

const currentMonth = ref(new Date())

const daysInMonth = computed(() => {
  const year = currentMonth.value.getFullYear()
  const month = currentMonth.value.getMonth()
  const days = new Date(year, month + 1, 0).getDate()
  const firstDay = new Date(year, month, 1).getDay()

  const daysArray = []
  for (let i = 0; i < firstDay; i++) {
    daysArray.push(null)
  }
  for (let i = 1; i <= days; i++) {
    daysArray.push(new Date(year, month, i))
  }
  return daysArray
})

const monthYear = computed(() => {
  return currentMonth.value.toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
})

const fetchRoomData = async () => {
  try {
    const roomId = route.params.id
    const [roomRes, reservationsRes] = await Promise.all([
      api.get(`/rooms/${roomId}`),
      api.get(`/reservations/room/${roomId}`)
    ])
    room.value = roomRes.data
    reservations.value = reservationsRes.data
  } catch (err) {
    error.value = 'Failed to fetch room data'
  } finally {
    loading.value = false
  }
}

const isDateReserved = (date: Date | null) => {
  if (!date) return false
  const dateStr = date.toISOString().split('T')[0]
  return reservations.value.some(r => {
    const start = new Date(r.start_date)
    const end = new Date(r.end_date)
    const current = new Date(dateStr)
    return current >= start && current < end
  })
}

const isDateSelected = (date: Date | null) => {
  if (!date) return false
  const dateStr = date.toISOString().split('T')[0]
  return selectedDates.value.includes(dateStr)
}

const toggleDateSelection = (date: Date | null) => {
  if (!date || isDateReserved(date)) return

  const dateStr = date.toISOString().split('T')[0]
  const index = selectedDates.value.indexOf(dateStr)

  if (index > -1) {
    selectedDates.value.splice(index, 1)
  } else {
    selectedDates.value.push(dateStr)
  }

  selectedDates.value.sort()

  if (selectedDates.value.length > 0) {
    startDate.value = selectedDates.value[0]
    const lastDate = new Date(selectedDates.value[selectedDates.value.length - 1])
    lastDate.setDate(lastDate.getDate() + 1)
    endDate.value = lastDate.toISOString().split('T')[0]
  }
}

const previousMonth = () => {
  currentMonth.value = new Date(currentMonth.value.getFullYear(), currentMonth.value.getMonth() - 1)
}

const nextMonth = () => {
  currentMonth.value = new Date(currentMonth.value.getFullYear(), currentMonth.value.getMonth() + 1)
}

const createReservation = async () => {
  if (!guestName.value || !guestEmail.value || selectedDates.value.length === 0) {
    error.value = 'Please fill all required fields and select dates'
    return
  }

  try {
    const reservation: CreateReservation = {
      room_id: Number(route.params.id),
      guest_name: guestName.value,
      guest_email: guestEmail.value,
      start_date: startDate.value,
      end_date: endDate.value,
      notes: notes.value || undefined
    }

    await api.post('/reservations', reservation)

    guestName.value = ''
    guestEmail.value = ''
    notes.value = ''
    startDate.value = ''
    endDate.value = ''
    selectedDates.value = []

    await fetchRoomData()
    error.value = ''
    alert('Reservation created successfully!')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to create reservation'
  }
}

onMounted(() => {
  fetchRoomData()
})
</script>

<template>
  <div class="min-h-screen bg-secondary-50">
    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>

    <div v-else-if="room">
      <div class="relative h-96 overflow-hidden">
        <img
          v-if="room.image_url"
          :src="room.image_url"
          :alt="room.name"
          class="w-full h-full object-cover"
        />
        <div v-else class="w-full h-full bg-gradient-to-br from-primary-400 to-primary-600"></div>
        <div class="absolute inset-0 bg-black bg-opacity-40 flex items-center justify-center">
          <div class="text-center text-white">
            <h1 class="text-5xl font-bold mb-4">{{ room.name }}</h1>
            <p v-if="room.description" class="text-xl">{{ room.description }}</p>
          </div>
        </div>
      </div>

      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
          <div>
            <div class="bg-white rounded-lg shadow-md p-6 mb-6">
              <h2 class="text-2xl font-semibold text-secondary-900 mb-4">
                Room Details
              </h2>
              <div class="space-y-3 text-secondary-700">
                <p><span class="font-semibold">Room Name:</span> {{ room.name }}</p>
                <p v-if="room.description"><span class="font-semibold">Description:</span> {{ room.description }}</p>
                <p><span class="font-semibold">Room ID:</span> {{ room.id }}</p>
              </div>
            </div>

            <div class="bg-white rounded-lg shadow-md p-6">
              <h2 class="text-xl font-semibold text-secondary-900 mb-4">
                Availability Calendar
              </h2>

              <div class="mb-4 flex items-center justify-between">
                <button
                  @click="previousMonth"
                  class="p-2 hover:bg-secondary-100 rounded-md transition"
                >
                  ←
                </button>
                <span class="font-semibold text-secondary-900">{{ monthYear }}</span>
                <button
                  @click="nextMonth"
                  class="p-2 hover:bg-secondary-100 rounded-md transition"
                >
                  →
                </button>
              </div>

              <div class="grid grid-cols-7 gap-1 mb-2">
                <div v-for="day in ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']"
                  :key="day"
                  class="text-center text-sm font-medium text-secondary-600 py-2"
                >
                  {{ day }}
                </div>
              </div>

              <div class="grid grid-cols-7 gap-1">
                <div
                  v-for="(date, index) in daysInMonth"
                  :key="index"
                  @click="toggleDateSelection(date)"
                  class="aspect-square flex items-center justify-center text-sm rounded-md transition"
                  :class="{
                    'bg-red-100 text-red-700 cursor-not-allowed': date && isDateReserved(date),
                    'bg-primary-600 text-white': date && isDateSelected(date),
                    'hover:bg-secondary-100 cursor-pointer': date && !isDateReserved(date) && !isDateSelected(date),
                    'text-secondary-900': date && !isDateReserved(date) && !isDateSelected(date),
                    'invisible': !date
                  }"
                >
                  {{ date?.getDate() }}
                </div>
              </div>

              <div class="mt-4 space-y-2 text-sm">
                <div class="flex items-center gap-2">
                  <div class="w-4 h-4 bg-red-100 border border-red-300 rounded"></div>
                  <span class="text-secondary-600">Reserved</span>
                </div>
                <div class="flex items-center gap-2">
                  <div class="w-4 h-4 bg-primary-600 rounded"></div>
                  <span class="text-secondary-600">Selected</span>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-white rounded-lg shadow-md p-6">
            <h2 class="text-xl font-semibold text-secondary-900 mb-4">
              Make a Reservation
            </h2>

            <form @submit.prevent="createReservation" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-secondary-700 mb-2">
                  Guest Name *
                </label>
                <input
                  v-model="guestName"
                  type="text"
                  required
                  class="w-full px-3 py-2 border border-secondary-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-secondary-700 mb-2">
                  Guest Email *
                </label>
                <input
                  v-model="guestEmail"
                  type="email"
                  required
                  class="w-full px-3 py-2 border border-secondary-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                />
              </div>

              <div>
                <label class="block text-sm font-medium text-secondary-700 mb-2">
                  Notes (Optional)
                </label>
                <textarea
                  v-model="notes"
                  rows="3"
                  placeholder="Add any special requests or notes..."
                  class="w-full px-3 py-2 border border-secondary-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
                ></textarea>
              </div>

              <div>
                <label class="block text-sm font-medium text-secondary-700 mb-2">
                  Selected Dates
                </label>
                <div class="px-3 py-2 border border-secondary-300 rounded-md bg-secondary-50 min-h-[42px]">
                  <span v-if="selectedDates.length > 0" class="text-secondary-900">
                    {{ selectedDates.length }} night(s) selected
                  </span>
                  <span v-else class="text-secondary-500">
                    Click on calendar to select dates
                  </span>
                </div>
              </div>

              <div v-if="error" class="bg-red-50 border border-red-300 text-red-700 px-4 py-3 rounded">
                {{ error }}
              </div>

              <button
                type="submit"
                class="w-full bg-primary-600 text-white py-3 rounded-md hover:bg-primary-700 transition disabled:opacity-50 font-semibold"
                :disabled="selectedDates.length === 0"
              >
                Reserve Room
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>