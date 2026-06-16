import { http } from './http'
import type { PackageGenerateRequest, PackageGenerateResponse } from '../types/package'

export async function generatePackage(payload: PackageGenerateRequest) {
  const { data } = await http.post<PackageGenerateResponse>('/api/package/generate', payload)
  return data
}

export async function getPackage(taskId: string) {
  const { data } = await http.get<PackageGenerateResponse>(`/api/package/${taskId}`)
  return data
}
