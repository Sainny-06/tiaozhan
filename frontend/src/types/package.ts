export interface StudentProfile {
  student_id: string
  major?: string
  grade?: string
  course?: string
  learning_goal?: string
  knowledge_level?: string
  math_level?: string
  coding_level?: string
  cognitive_style?: string[]
  weak_points?: string[]
  resource_preference?: string[]
  mastery?: Record<string, string>
}

export interface SourceRef {
  file: string
  section: string
  reason?: string
}

export interface ReviewReport {
  knowledge_grounding: string
  difficulty_match: string
  answer_consistency: string
  content_safety: string
  comment: string
}

export interface LearningResource {
  resource_id?: string
  type: 'lecture' | 'mindmap' | 'quiz' | 'code_lab' | 'animation' | string
  title: string
  content?: string
  mermaid_code?: string
  code?: string
  steps?: string[]
  questions?: Array<Record<string, unknown>>
  source_refs: SourceRef[]
  review_report: ReviewReport
}

export interface LearningPathItem {
  step: number
  title: string
  recommended_resources: string[]
  reason: string
}

export interface PackageGenerateRequest {
  student_id: string
  dialogue: string
  target_course: string
  target_topic: string
}

export interface AgentOutput {
  agent: string
  agent_log: string
  [key: string]: unknown
}

export interface PackageGenerateResponse {
  task_id: string
  status: string
  target_course?: string
  target_topic?: string
  profile_agent_output: AgentOutput
  retrieval_agent_output: AgentOutput
  resource_agent_output: AgentOutput
  review_path_agent_output: AgentOutput
  resources: LearningResource[]
  learning_path: LearningPathItem[]
}
