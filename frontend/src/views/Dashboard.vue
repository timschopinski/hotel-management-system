<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../api'
import type { Room } from '../types'

const rooms = ref<Room[]>([])
const newRoomName = ref('')
const newRoomDescription = ref('')
const newRoomImageUrl = ref('')
const loading = ref(true)
const error = ref('')
const editingRoom = ref<Room | null>(null)

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
    await api.post('/rooms', {
      name: newRoomName.value,
      description: newRoomDescription.value || null,
      image_url: newRoomImageUrl.value || null
    })
    newRoomName.value = ''
    newRoomDescription.value = ''
    newRoomImageUrl.value = ''
    await fetchMyRooms()
  } catch (err) {
    error.value = 'Failed to create room'
  }
}

const startEdit = (room: Room) => {
  editingRoom.value = { ...room }
}

const cancelEdit = () => {
  editingRoom.value = null
}

const saveEdit = async () => {
  if (!editingRoom.value) return

  try {
    await api.patch(`/rooms/${editingRoom.value.id}`, {
      name: editingRoom.value.name,
      description: editingRoom.value.description,
      image_url: editingRoom.value.image_url
    })
    editingRoom.value = null
    await fetchMyRooms()
  } catch (err) {
    error.value = 'Failed to update room'
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
      Admin Dashboard
    </h1>

    <div class="bg-white rounded-lg shadow-md p-6 mb-8">
      <h2 class="text-xl font-semibold text-secondary-900 mb-4">
        Add New Room
      </h2>
      <div class="space-y-4">
        <input
          v-model="newRoomName"
          type="text"
          placeholder="Room name"
          class="w-full px-3 py-2 border border-secondary-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
        />
        <textarea
          v-model="newRoomDescription"
          placeholder="Room description"
          rows="3"
          class="w-full px-3 py-2 border border-secondary-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
        ></textarea>
        <input
          v-model="newRoomImageUrl"
          type="url"
          placeholder="Image URL (e.g., https://images.unsplash.com/...)"
          class="w-full px-3 py-2 border border-secondary-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
        />
        <button
          @click="createRoom"
          class="w-full bg-primary-600 text-white px-6 py-2 rounded-md hover:bg-primary-700 transition"
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
          class="border border-secondary-200 rounded-lg p-4"
        >
          <template v-if="editingRoom?.id === room.id">
            <div class="space-y-3">
              <input
                v-model="editingRoom.name"
                type="text"
                class="w-full px-3 py-2 border border-secondary-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
              <textarea
                v-model="editingRoom.description"
                rows="2"
                class="w-full px-3 py-2 border border-secondary-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              ></textarea>
              <input
                v-model="editingRoom.image_url"
                type="url"
                placeholder="Image URL"
                class="w-full px-3 py-2 border border-secondary-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500"
              />
              <div class="flex gap-2">
                <button
                  @click="saveEdit"
                  class="flex-1 bg-green-600 text-white px-4 py-2 rounded-md hover:bg-green-700 transition"
                >
                  Save
                </button>
                <button
                  @click="cancelEdit"
                  class="flex-1 bg-secondary-600 text-white px-4 py-2 rounded-md hover:bg-secondary-700 transition"
                >
                  Cancel
                </button>
              </div>
            </div>
          </template>
          <template v-else>
            <div class="flex items-start gap-4">
              <div v-if="room.image_url" class="flex-shrink-0 w-24 h-24 rounded overflow-hidden">
                <img :src="room.image_url" :alt="room.name" class="w-full h-full object-cover" />
              </div>
              <div class="flex-1">
                <h3 class="font-semibold text-secondary-900 text-lg">{{ room.name }}</h3>
                <p v-if="room.description" class="text-sm text-secondary-600 mt-1">{{ room.description }}</p>
              </div>
              <div class="flex gap-2">
                <button
                  @click="startEdit(room)"
                  class="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 transition"
                >
                  Edit
                </button>
                <button
                  @click="deleteRoom(room.id)"
                  class="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700 transition"
                >
                  Delete
                </button>
              </div>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>