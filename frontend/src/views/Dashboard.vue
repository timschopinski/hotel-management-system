<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../api'
import type { Room } from '../types'

const rooms = ref<Room[]>([])
const newRoomName = ref('')
const loading = ref(true)
const error = ref('')

const fetchMyRooms = async () => {
  try {
    const response = await api.get('/rooms/my')
    rooms.value = response.data
  } catch (err) {
    error.value = 'Failed to fetch rooms'
  } finally {
    loading.value = false
  }
}

const createRoom = async () => {
  if (!newRoomName.value.trim()) return

  try {
    await api.post('/rooms', { name: newRoomName.value })
    newRoomName.value = ''
    await fetchMyRooms()
  } catch (err) {
    error.value = 'Failed to create room'
  }
}

const deleteRoom = async (roomId: number) => {
  if (!confirm('Are you sure you want to delete this room?')) return

  try {
    await api.delete(`/rooms/${roomId}`)
    await fetchMyRooms()
  } catch (err) {
    error.value = 'Failed to delete room'
  }
}

onMounted(() => {
  fetchMyRooms()
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
    <h1 class="text-3xl font-bold text-secondary-900 mb-8">
      Dashboard
    </h1>

    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 class="text-xl font-semibold text-secondary-900 mb-4">
        Add New Room
      </h2>
      <div class="flex gap-4">
        <input
          v-model="newRoomName"
          type="text"
          placeholder="Room name"
          class="flex-1 px-3 py-2 border border-secondary-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
          @keyup.enter="createRoom"
        />
        <button
          @click="createRoom"
          class="bg-primary-600 text-white px-6 py-2 rounded-md hover:bg-primary-700 transition"
        >
          Add Room
        </button>
      </div>
    </div>

    <div v-if="error" class="bg-red-50 border border-red-300 text-red-700 px-4 py-3 rounded mb-6">
      {{ error }}
    </div>

    <div class="bg-white rounded-lg shadow-md p-6">
      <h2 class="text-xl font-semibold text-secondary-900 mb-4">
        My Rooms
      </h2>

      <div v-if="loading" class="text-center py-8">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>

      <div v-else-if="rooms.length === 0" class="text-center py-8 text-secondary-600">
        You haven't created any rooms yet
      </div>

      <div v-else class="space-y-4">
        <div
          v-for="room in rooms"
          :key="room.id"
          class="flex items-center justify-between p-4 border border-secondary-200 rounded-lg hover:bg-secondary-50 transition"
        >
          <div>
            <h3 class="font-semibold text-secondary-900">{{ room.name }}</h3>
            <p class="text-sm text-secondary-600">Room ID: {{ room.id }}</p>
          </div>
          <button
            @click="deleteRoom(room.id)"
            class="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition"
          >
            Delete
          </button>
        </div>
      </div>
    </div>
  </div>
</template>