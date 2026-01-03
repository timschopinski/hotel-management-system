<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api'
import type { Room } from '../types'

const rooms = ref<Room[]>([])
const loading = ref(true)
const router = useRouter()

const fetchRooms = async () => {
  try {
    const response = await api.get('/rooms')
    rooms.value = response.data
  } catch (error) {
    console.error('Failed to fetch rooms', error)
  } finally {
    loading.value = false
  }
}

const goToRoom = (roomId: number) => {
  router.push(`/room/${roomId}`)
}

onMounted(() => {
  fetchRooms()
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <div class="text-center mb-12">
      <h1 class="text-4xl font-bold text-secondary-900 mb-4">
        Available Rooms
      </h1>
      <p class="text-lg text-secondary-600">
        Browse our selection of hotel rooms and make a reservation
      </p>
    </div>

    <div v-if="loading" class="text-center py-12">
      <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
    </div>

    <div v-else-if="rooms.length === 0" class="text-center py-12">
      <p class="text-secondary-600 text-lg">No rooms available at the moment</p>
    </div>

    <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        v-for="room in rooms"
        :key="room.id"
        class="bg-white rounded-lg shadow-md hover:shadow-xl transition cursor-pointer overflow-hidden"
        @click="goToRoom(room.id)"
      >
        <div class="h-48 bg-gradient-to-br from-primary-400 to-primary-600"></div>
        <div class="p-6">
          <h2 class="text-xl font-semibold text-secondary-900 mb-2">
            {{ room.name }}
          </h2>
          <p class="text-secondary-600 text-sm mb-4">
            Room ID: {{ room.id }}
          </p>
          <button class="w-full bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 transition">
            View Details
          </button>
        </div>
      </div>
    </div>
  </div>
</template>