import axios from 'axios'

export const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8001',
  timeout: 15000,
})

export interface HealthResponse {
  status: string
  service: string
}

export async function getHealth() {
  const { data } = await http.get<HealthResponse>('/health')
  return data
}
