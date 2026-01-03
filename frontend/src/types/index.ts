export interface User {
  id: number
  email: string
  created_at: string
}

export interface Room {
  id: number
  name: string
  owner_id: number
  created_at: string
}

export interface Reservation {
  id: number
  room_id: number
  guest_name: string
  guest_email: string
  start_date: string
  end_date: string
  created_at: string
  room?: Room
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterCredentials {
  email: string
  password: string
}

export interface CreateRoom {
  name: string
}

export interface CreateReservation {
  room_id: number
  guest_name: string
  guest_email: string
  start_date: string
  end_date: string
}