import type { LearningPathItem, StudentProfile } from './package'

export interface QuizAnswerItem {
  question_id: string
  student_answer: string
}

export interface QuizSubmitRequest {
  student_id: string
  topic: string
  answers: QuizAnswerItem[]
  task_id?: string
}

export interface WrongQuestionAnalysis {
  question_id: string
  knowledge_point: string
  student_answer: string
  correct_answer: string | null
  is_correct: boolean
  error_type: string
  explanation: string
}

export interface RecommendationItem {
  title: string
  type: string
  reason: string
}

export interface ProfileDiffItem {
  field: string
  before: unknown
  after: unknown
  reason: string
}

export interface QuizSubmitResponse {
  record_id: string
  score: number
  total_questions: number
  correct_count: number
  wrong_points: string[]
  wrong_question_analysis: WrongQuestionAnalysis[]
  profile_before: StudentProfile
  profile_after: StudentProfile
  profile_diff: ProfileDiffItem[]
  new_recommendations: RecommendationItem[]
  updated_learning_path: LearningPathItem[]
}

export interface QuizRecord extends QuizSubmitResponse {
  student_id: string
  topic: string
}
