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
  <div class="min-h-screen bg-secondary-50">
    <div class="relative h-96 bg-gradient-to-r from-primary-600 to-primary-800 overflow-hidden">
      <div class="absolute inset-0 bg-black opacity-20"></div>
      <div class="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-full flex items-center">
        <div class="text-white">
          <h1 class="text-5xl font-bold mb-4">Welcome to Grand Hotel</h1>
          <p class="text-xl mb-8 text-primary-100">Experience luxury and comfort in our premium rooms</p>
          <a href="#rooms" class="bg-white text-primary-600 px-8 py-3 rounded-lg font-semibold hover:bg-primary-50 transition inline-block">
            Explore Rooms
          </a>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div class="text-center mb-12">
        <h2 class="text-3xl font-bold text-secondary-900 mb-4">Our Amenities</h2>
        <p class="text-lg text-secondary-600">Everything you need for a perfect stay</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-8 mb-20">
        <div class="text-center p-6">
          <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold mb-2">24/7 Service</h3>
          <p class="text-secondary-600">Round the clock assistance for all your needs</p>
        </div>

        <div class="text-center p-6">
          <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold mb-2">Premium Rooms</h3>
          <p class="text-secondary-600">Luxurious accommodations with modern amenities</p>
        </div>

        <div class="text-center p-6">
          <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <svg class="w-8 h-8 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 10h4.764a2 2 0 011.789 2.894l-3.5 7A2 2 0 0115.263 21h-4.017c-.163 0-.326-.02-.485-.06L7 20m7-10V5a2 2 0 00-2-2h-.095c-.5 0-.905.405-.905.905 0 .714-.211 1.412-.608 2.006L7 11v9m7-10h-2M7 20H5a2 2 0 01-2-2v-6a2 2 0 012-2h2.5"></path>
            </svg>
          </div>
          <h3 class="text-xl font-semibold mb-2">Best Experience</h3>
          <p class="text-secondary-600">Unforgettable moments and exceptional service</p>
        </div>
      </div>

      <div id="rooms" class="scroll-mt-20">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-secondary-900 mb-4">Available Rooms</h2>
          <p class="text-lg text-secondary-600">Choose from our selection of premium accommodations</p>
        </div>

        <div v-if="loading" class="text-center py-12">
          <div class="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>

        <div v-else-if="rooms.length === 0" class="text-center py-12 bg-white rounded-lg shadow-md">
          <p class="text-secondary-600 text-lg">No rooms available at the moment</p>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          <div
            v-for="room in rooms"
            :key="room.id"
            class="bg-white rounded-lg shadow-md hover:shadow-2xl transition-all duration-300 cursor-pointer overflow-hidden group"
            @click="goToRoom(room.id)"
          >
            <div class="relative h-56 overflow-hidden">
              <img
                v-if="room.image_url"
                :src="room.image_url"
                :alt="room.name"
                class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300"
              />
              <div v-else class="w-full h-full bg-gradient-to-br from-primary-400 to-primary-600 group-hover:from-primary-500 group-hover:to-primary-700 transition-all duration-300"></div>
            </div>
            <div class="p-6">
              <h3 class="text-xl font-semibold text-secondary-900 mb-2">
                {{ room.name }}
              </h3>
              <p v-if="room.description" class="text-secondary-600 text-sm mb-4 line-clamp-2">
                {{ room.description }}
              </p>
              <button class="w-full bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700 transition">
                View Details & Book
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <footer class="bg-secondary-800 text-white py-12 mt-20">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <h3 class="text-xl font-bold mb-4">Grand Hotel</h3>
            <p class="text-secondary-300">Experience luxury and comfort at its finest</p>
          </div>
          <div>
            <h3 class="text-xl font-bold mb-4">Contact</h3>
            <p class="text-secondary-300">Email: info@grandhotel.com</p>
            <p class="text-secondary-300">Phone: +1 234 567 890</p>
          </div>
          <div>
            <h3 class="text-xl font-bold mb-4">Location</h3>
            <p class="text-secondary-300">123 Luxury Street</p>
            <p class="text-secondary-300">Grand City, GC 12345</p>
          </div>
        </div>
        <div class="border-t border-secondary-700 mt-8 pt-8 text-center text-secondary-400">
          <p>&copy; 2026 Grand Hotel. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>