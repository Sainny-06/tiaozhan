<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

import { loadRecentPackage } from '../api/packageStore'
import type { PackageGenerateResponse } from '../types/package'

const router = useRouter()
const packageResult = ref<PackageGenerateResponse | null>(loadRecentPackage())
const learningPath = computed(() => packageResult.value?.learning_path ?? [])
</script>

<template>
  <section class="page">
    <h1 class="page-title">个性化学习路径</h1>
    <p class="page-copy">
      根据学生画像、目标主题、检索知识点和生成资源，展示后端规划出的学习步骤。
    </p>

    <div v-if="!packageResult" class="panel empty-panel">
      <el-empty description="还没有学习路径">
        <el-button type="primary" @click="router.push('/')">先生成资源包</el-button>
      </el-empty>
    </div>

    <div v-else class="path-shell">
      <div class="path-summary">
        <span>task_id</span>
        <strong>{{ packageResult.task_id }}</strong>
      </div>

      <div class="path-list">
        <article v-for="item in learningPath" :key="item.step" class="path-card">
          <div class="step-index">{{ item.step }}</div>
          <div class="step-content">
            <h2>{{ item.title }}</h2>
            <p>{{ item.reason }}</p>
            <div class="resource-tags">
              <span v-for="resource in item.recommended_resources" :key="resource">
                {{ resource }}
              </span>
            </div>
          </div>
        </article>
      </div>
    </div>
  </section>
</template>

<style scoped>
.empty-panel {
  margin-top: 36px;
}

.path-shell {
  margin-top: 36px;
}

.path-summary {
  padding: 20px;
  border: 1px solid rgba(16, 24, 40, 0.08);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.86);
  box-shadow: 0 20px 56px rgba(31, 41, 55, 0.08);
}

.path-summary span {
  display: block;
  margin-bottom: 8px;
  color: #667085;
  font-size: 14px;
}

.path-summary strong {
  color: #101828;
  word-break: break-all;
}

.path-list {
  display: grid;
  gap: 18px;
  margin-top: 24px;
}

.path-card {
  display: grid;
  grid-template-columns: 56px minmax(0, 1fr);
  gap: 18px;
  padding: 24px;
  border: 1px solid rgba(16, 24, 40, 0.08);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 20px 56px rgba(31, 41, 55, 0.08);
}

.step-index {
  display: grid;
  place-items: center;
  width: 44px;
  height: 44px;
  border-radius: 999px;
  background: #17202a;
  color: #ffffff;
  font-weight: 850;
}

.step-content h2 {
  margin: 0 0 10px;
  color: #101828;
  font-size: 24px;
}

.step-content p {
  margin: 0;
  color: #475467;
  line-height: 1.8;
}

.resource-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 14px;
}

.resource-tags span {
  padding: 6px 10px;
  border-radius: 999px;
  background: #edf3ff;
  color: #2f5fb8;
  font-size: 13px;
}
</style>
