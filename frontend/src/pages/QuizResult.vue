<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

import ProfileCompareTable from '../components/ProfileCompareTable.vue'
import { loadRecentPackage } from '../api/packageStore'
import { submitQuiz } from '../api/quiz'
import type { LearningResource, PackageGenerateResponse, StudentProfile } from '../types/package'
import type { QuizSubmitResponse } from '../types/quiz'

interface QuizQuestion {
  question_id: string
  question_type: string
  question: string
  options: Record<string, string>
  answer: string
  explanation: string
  knowledge_point: string
  difficulty: string
}

const router = useRouter()
const packageResult = ref<PackageGenerateResponse | null>(loadRecentPackage())
const answers = ref<Record<string, string>>({})
const submitting = ref(false)
const result = ref<QuizSubmitResponse | null>(null)
const errorMessage = ref('')

const quizResource = computed<LearningResource | null>(() => {
  return packageResult.value?.resources.find((resource) => resource.type === 'quiz') ?? null
})

const questions = computed<QuizQuestion[]>(() => {
  return (quizResource.value?.questions ?? []) as unknown as QuizQuestion[]
})

const canSubmit = computed(() => Boolean(packageResult.value && questions.value.length))

function optionEntries(options: Record<string, string>) {
  return Object.entries(options)
}

function fillWrongDemo() {
  const nextAnswers: Record<string, string> = {}

  for (const question of questions.value) {
    nextAnswers[question.question_id] = question.answer

    if (question.knowledge_point === 'Sigmoid 函数') {
      nextAnswers[question.question_id] = question.answer === 'C' ? 'B' : 'C'
    }
    if (question.knowledge_point === '逻辑回归损失函数') {
      nextAnswers[question.question_id] = question.answer === 'A' ? 'C' : 'A'
    }
  }

  answers.value = nextAnswers
  ElMessage.success('已自动答对其他题，并故意答错 Sigmoid 和损失函数')
}

function fillAllCorrect() {
  const nextAnswers: Record<string, string> = {}
  for (const question of questions.value) {
    nextAnswers[question.question_id] = question.answer
  }
  answers.value = nextAnswers
  ElMessage.success('已填入全部正确答案')
}

async function submitCurrentQuiz() {
  if (!packageResult.value) {
    ElMessage.warning('请先生成资源包')
    return
  }

  submitting.value = true
  errorMessage.value = ''

  try {
    const profile = packageResult.value.profile_agent_output.profile as StudentProfile | undefined
    result.value = await submitQuiz({
      task_id: packageResult.value.task_id,
      student_id: profile?.student_id || 'stu_001',
      topic: packageResult.value.target_topic || '逻辑回归',
      answers: Object.entries(answers.value).map(([question_id, student_answer]) => ({
        question_id,
        student_answer,
      })),
    })
    ElMessage.success('测验提交成功')
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '测验提交失败'
    ElMessage.error('测验提交失败')
  } finally {
    submitting.value = false
  }
}
</script>

<template>
  <section class="page">
    <h1 class="page-title">测验提交与画像更新</h1>
    <p class="page-copy">
      从最近一次资源包中读取分层题库，提交后展示评分、错题分析、画像更新、新推荐资源与调整后的路径。
    </p>

    <div v-if="!packageResult || !quizResource" class="panel empty-panel">
      <el-empty description="还没有可提交的测验">
        <el-button type="primary" @click="router.push('/')">先生成资源包</el-button>
      </el-empty>
    </div>

    <template v-else>
      <div class="quiz-summary">
        <div>
          <span>task_id</span>
          <strong>{{ packageResult.task_id }}</strong>
        </div>
        <div>
          <span>题目数量</span>
          <strong>{{ questions.length }}</strong>
        </div>
      </div>

      <div class="panel quiz-panel">
        <div class="quiz-actions">
          <el-button @click="fillWrongDemo">故意答错 Sigmoid 和损失函数</el-button>
          <el-button @click="fillAllCorrect">填入全部正确答案</el-button>
          <el-button type="primary" :loading="submitting" :disabled="!canSubmit" @click="submitCurrentQuiz">
            提交测验
          </el-button>
        </div>

        <el-alert
          v-if="errorMessage"
          class="status-alert"
          type="error"
          :title="errorMessage"
          :closable="false"
          show-icon
        />

        <div class="question-list">
          <article v-for="question in questions" :key="question.question_id" class="question-card">
            <div class="question-meta">
              <span>{{ question.knowledge_point }}</span>
              <span>{{ question.difficulty }}</span>
            </div>
            <h2>{{ question.question }}</h2>
            <el-radio-group v-model="answers[question.question_id]" class="option-group">
              <el-radio
                v-for="[key, value] in optionEntries(question.options)"
                :key="key"
                :value="key"
                border
              >
                {{ key }}. {{ value }}
              </el-radio>
            </el-radio-group>
          </article>
        </div>
      </div>

      <div v-if="result" class="result-stack">
        <div class="score-grid">
          <div>
            <span>得分</span>
            <strong>{{ result.score }}</strong>
          </div>
          <div>
            <span>总题数</span>
            <strong>{{ result.total_questions }}</strong>
          </div>
          <div>
            <span>答对题数</span>
            <strong>{{ result.correct_count }}</strong>
          </div>
        </div>

        <div class="panel">
          <h2 class="section-title">错题知识点</h2>
          <div v-if="result.wrong_points.length" class="tag-group">
            <span v-for="point in result.wrong_points" :key="point">{{ point }}</span>
          </div>
          <el-empty v-else description="没有错题知识点" />
        </div>

        <div class="panel">
          <h2 class="section-title">错题分析</h2>
          <el-table :data="result.wrong_question_analysis" border>
            <el-table-column prop="question_id" label="题目 ID" min-width="180" />
            <el-table-column prop="knowledge_point" label="知识点" min-width="180" />
            <el-table-column prop="student_answer" label="学生答案" min-width="100" />
            <el-table-column prop="correct_answer" label="正确答案" min-width="100" />
            <el-table-column prop="error_type" label="错误类型" min-width="140" />
            <el-table-column prop="explanation" label="解析" min-width="260" />
          </el-table>
        </div>

        <div class="panel">
          <h2 class="section-title">画像更新前后对比</h2>
          <ProfileCompareTable :diffs="result.profile_diff" />
        </div>

        <div class="panel profile-json-grid">
          <div>
            <h2 class="section-title">更新前画像</h2>
            <pre class="result-box">{{ JSON.stringify(result.profile_before, null, 2) }}</pre>
          </div>
          <div>
            <h2 class="section-title">更新后画像</h2>
            <pre class="result-box">{{ JSON.stringify(result.profile_after, null, 2) }}</pre>
          </div>
        </div>

        <div class="panel">
          <h2 class="section-title">新增推荐资源</h2>
          <div class="recommendation-grid">
            <article v-for="item in result.new_recommendations" :key="item.title">
              <span>{{ item.type }}</span>
              <h3>{{ item.title }}</h3>
              <p>{{ item.reason }}</p>
            </article>
          </div>
        </div>

        <div class="panel">
          <h2 class="section-title">调整后的学习路径</h2>
          <div class="updated-path-list">
            <article v-for="item in result.updated_learning_path" :key="item.step">
              <strong>{{ item.step }}</strong>
              <div>
                <h3>{{ item.title }}</h3>
                <p>{{ item.reason }}</p>
                <div class="tag-group compact">
                  <span v-for="resource in item.recommended_resources" :key="resource">{{ resource }}</span>
                </div>
              </div>
            </article>
          </div>
        </div>
      </div>
    </template>
  </section>
</template>

<style scoped>
.empty-panel {
  margin-top: 36px;
}

.quiz-summary,
.score-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  margin-top: 36px;
}

.quiz-summary {
  grid-template-columns: minmax(0, 1fr) 180px;
}

.quiz-summary div,
.score-grid div {
  padding: 20px;
  border: 1px solid rgba(16, 24, 40, 0.08);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.86);
  box-shadow: 0 20px 56px rgba(31, 41, 55, 0.08);
}

.quiz-summary span,
.score-grid span {
  display: block;
  margin-bottom: 8px;
  color: #667085;
}

.quiz-summary strong,
.score-grid strong {
  color: #101828;
  font-size: 28px;
  word-break: break-all;
}

.quiz-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.status-alert {
  margin-top: 16px;
}

.question-list {
  display: grid;
  gap: 16px;
  margin-top: 22px;
}

.question-card {
  padding: 20px;
  border: 1px solid rgba(16, 24, 40, 0.08);
  border-radius: 8px;
  background: #f8fbff;
}

.question-meta {
  display: flex;
  gap: 8px;
  margin-bottom: 10px;
}

.question-meta span,
.tag-group span,
.recommendation-grid span {
  padding: 6px 10px;
  border-radius: 999px;
  background: #edf3ff;
  color: #2f5fb8;
  font-size: 13px;
}

.question-card h2 {
  margin: 0 0 14px;
  color: #101828;
  font-size: 20px;
  line-height: 1.6;
}

.option-group {
  display: grid;
  gap: 10px;
}

.option-group :deep(.el-radio) {
  width: 100%;
  height: auto;
  min-height: 44px;
  margin-right: 0;
  padding: 10px 12px;
  white-space: normal;
}

.result-stack {
  display: grid;
  gap: 24px;
  margin-top: 28px;
}

.section-title {
  margin: 0 0 18px;
  color: #101828;
  font-size: 24px;
}

.tag-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-group.compact {
  margin-top: 10px;
}

.profile-json-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}

.recommendation-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
}

.recommendation-grid article {
  padding: 18px;
  border: 1px solid rgba(16, 24, 40, 0.08);
  border-radius: 8px;
  background: #f8fbff;
}

.recommendation-grid h3,
.updated-path-list h3 {
  margin: 12px 0 8px;
  color: #101828;
}

.recommendation-grid p,
.updated-path-list p {
  margin: 0;
  color: #475467;
  line-height: 1.7;
}

.updated-path-list {
  display: grid;
  gap: 14px;
}

.updated-path-list article {
  display: grid;
  grid-template-columns: 44px minmax(0, 1fr);
  gap: 14px;
  padding: 18px;
  border-radius: 8px;
  background: #f8fbff;
}

.updated-path-list article > strong {
  display: grid;
  place-items: center;
  width: 36px;
  height: 36px;
  border-radius: 999px;
  background: #17202a;
  color: #ffffff;
}

@media (max-width: 860px) {
  .quiz-summary,
  .score-grid,
  .profile-json-grid {
    grid-template-columns: 1fr;
  }
}
</style>
