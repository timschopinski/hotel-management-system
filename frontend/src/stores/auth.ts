import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api'
import type { User, LoginCredentials, RegisterCredentials } from '../types'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const user = ref<User | null>(null)

  const login = async (credentials: LoginCredentials) => {
    const response = await api.post('/auth/login', credentials)
    token.value = response.data.access_token
    localStorage.setItem('token', response.data.access_token)
    await fetchUser()
  }

  const register = async (credentials: RegisterCredentials) => {
    await api.post('/auth/register', credentials)
  }

  const logout = () => {
    token.value = null
    user.value = null
    localStorage.removeItem('token')
  }

  const fetchUser = async () => {
    if (!token.value) return
    try {
      const response = await api.get('/auth/me')
      user.value = response.data
    } catch (error) {
      logout()
    }
  }

  if (token.value) {
    fetchUser()
  }

  return {
    token,
    user,
    login,
    register,
    logout,
    fetchUser
  }
})