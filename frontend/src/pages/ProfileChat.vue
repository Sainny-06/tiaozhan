<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

import { getHealth, type HealthResponse } from '../api/http'
import { generatePackage } from '../api/package'
import { loadRecentPackage, saveRecentPackage } from '../api/packageStore'
import type { PackageGenerateResponse, StudentProfile } from '../types/package'

const router = useRouter()

const demoText =
  '我是人工智能专业大二学生，正在学习机器学习。逻辑回归里的 sigmoid 和损失函数看不懂。我的数学基础一般，但 Python 还可以。希望系统用图解和代码案例帮我学习。'

const studentId = ref('stu_001')
const targetCourse = ref('机器学习基础')
const targetTopic = ref('逻辑回归')
const dialogue = ref('')
const loading = ref(false)
const healthLoading = ref(false)
const health = ref<HealthResponse | null>(null)
const errorMessage = ref('')
const packageResult = ref<PackageGenerateResponse | null>(loadRecentPackage())

const profile = computed<StudentProfile | null>(() => {
  return (packageResult.value?.profile_agent_output.profile as StudentProfile | undefined) ?? null
})

function fillDemoText() {
  dialogue.value = demoText
}

async function submitPackage() {
  if (!dialogue.value.trim()) {
    ElMessage.warning('请先输入学习需求，或使用演示文本。')
    return
  }

  loading.value = true
  errorMessage.value = ''

  try {
    const result = await generatePackage({
      student_id: studentId.value,
      dialogue: dialogue.value,
      target_course: targetCourse.value,
      target_topic: targetTopic.value,
    })
    packageResult.value = result
    saveRecentPackage(result)
    ElMessage.success('资源包生成成功，正在进入 Agent 流程页。')
    await router.push('/generate')
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '资源包生成失败'
    ElMessage.error('资源包生成失败')
  } finally {
    loading.value = false
  }
}

async function checkBackend() {
  healthLoading.value = true
  errorMessage.value = ''
  health.value = null

  try {
    health.value = await getHealth()
    ElMessage.success('后端连接成功')
  } catch (error) {
    errorMessage.value = error instanceof Error ? error.message : '后端连接失败'
    ElMessage.error('后端连接失败')
  } finally {
    healthLoading.value = false
  }
}
</script>

<template>
  <section class="page">
    <h1 class="page-title">从学习需求生成个性化资源包</h1>
    <p class="page-copy">
      输入学生的自然语言学习需求，后端会依次运行 Profile、Retrieval、Resource、ReviewPath 四个 Agent。
    </p>

    <div class="profile-layout">
      <div class="panel input-panel">
        <div class="field-grid">
          <el-input v-model="studentId" size="large" placeholder="学生 ID" />
          <el-input v-model="targetCourse" size="large" placeholder="目标课程" />
          <el-input v-model="targetTopic" size="large" placeholder="目标主题" />
        </div>

        <el-input
          v-model="dialogue"
          class="dialogue-input"
          type="textarea"
          :rows="8"
          resize="none"
          placeholder="请输入学生学习需求，例如：我正在学习逻辑回归，Sigmoid 和损失函数看不懂..."
        />

        <div class="action-row">
          <el-button size="large" @click="fillDemoText">填充演示文本</el-button>
          <el-button type="primary" size="large" :loading="loading" @click="submitPackage">
            生成个性化学习资源包
          </el-button>
        </div>

        <el-alert
          v-if="errorMessage"
          class="status-alert"
          type="error"
          :title="errorMessage"
          show-icon
          :closable="false"
        />

        <div class="health-check">
          <el-button :loading="healthLoading" @click="checkBackend">检查后端连接</el-button>
          <pre v-if="health" class="result-box">{{ JSON.stringify(health, null, 2) }}</pre>
        </div>
      </div>

      <aside class="panel profile-card">
        <div class="card-header">
          <span>学生画像</span>
          <small v-if="packageResult">task_id: {{ packageResult.task_id }}</small>
        </div>

        <el-empty v-if="!profile" description="生成资源包后展示画像" />
        <dl v-else class="profile-list">
          <div>
            <dt>专业背景</dt>
            <dd>{{ profile.major }}</dd>
          </div>
          <div>
            <dt>年级</dt>
            <dd>{{ profile.grade }}</dd>
          </div>
          <div>
            <dt>课程</dt>
            <dd>{{ profile.course }}</dd>
          </div>
          <div>
            <dt>学习目标</dt>
            <dd>{{ profile.learning_goal }}</dd>
          </div>
          <div>
            <dt>数学能力</dt>
            <dd>{{ profile.math_level }}</dd>
          </div>
          <div>
            <dt>编程能力</dt>
            <dd>{{ profile.coding_level }}</dd>
          </div>
        </dl>

        <div v-if="profile" class="tag-group">
          <span v-for="point in profile.weak_points" :key="point">{{ point }}</span>
        </div>
      </aside>
    </div>
  </section>
</template>

<style scoped>
.profile-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(320px, 0.65fr);
  gap: 24px;
  align-items: start;
}

.field-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.dialogue-input {
  margin-top: 18px;
}

.action-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 18px;
}

.status-alert,
.health-check {
  margin-top: 18px;
}

.card-header {
  display: flex;
  align-items: baseline;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
  color: #101828;
  font-weight: 800;
}

.card-header small {
  color: #667085;
  font-size: 12px;
  font-weight: 500;
}

.profile-list {
  display: grid;
  gap: 14px;
  margin: 0;
}

.profile-list div {
  display: grid;
  grid-template-columns: 92px minmax(0, 1fr);
  gap: 12px;
}

.profile-list dt {
  color: #667085;
}

.profile-list dd {
  margin: 0;
  color: #101828;
  font-weight: 650;
}

.tag-group {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 18px;
}

.tag-group span {
  padding: 7px 10px;
  border-radius: 999px;
  background: #edf3ff;
  color: #2f5fb8;
  font-size: 13px;
}

@media (max-width: 900px) {
  .profile-layout,
  .field-grid {
    grid-template-columns: 1fr;
  }
}
</style>
