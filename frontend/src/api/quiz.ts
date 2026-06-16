import { http } from './http'
import type { QuizRecord, QuizSubmitRequest, QuizSubmitResponse } from '../types/quiz'
import type { StudentProfile } from '../types/package'

export async function submitQuiz(payload: QuizSubmitRequest) {
  const { data } = await http.post<QuizSubmitResponse>('/api/quiz/submit', payload)
  return data
}

export async function getProfile(studentId: string) {
  const { data } = await http.get<StudentProfile>(`/api/profile/${studentId}`)
  return data
}

export async function getQuizRecord(recordId: string) {
  const { data } = await http.get<QuizRecord>(`/api/quiz/${recordId}`)
  return data
}
