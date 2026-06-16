import { http } from './http'

export interface KnowledgeIndexSummary {
  course_id: string
  course_name: string
  course_level: string
  description: string
  chapter_count: number
  chapters: Array<{
    chapter_id: string
    title: string
    file_path: string
    difficulty: string
    knowledge_points: string[]
  }>
}

export interface KnowledgeChapterResponse {
  found: boolean
  chapter?: Record<string, unknown>
  content?: string
  sections?: Record<string, string>
  message?: string
}

export async function getKnowledgeIndex() {
  const { data } = await http.get<KnowledgeIndexSummary>('/api/knowledge/index')
  return data
}

export async function getKnowledgeChapter(chapterId: string) {
  const { data } = await http.get<KnowledgeChapterResponse>(`/api/knowledge/chapter/${chapterId}`)
  return data
}
