<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

import ResourceCard from '../components/ResourceCard.vue'
import { loadRecentPackage } from '../api/packageStore'
import type { LearningResource, PackageGenerateResponse } from '../types/package'

const router = useRouter()
const packageResult = ref<PackageGenerateResponse | null>(loadRecentPackage())

const resources = computed<LearningResource[]>(() => packageResult.value?.resources ?? [])
const resourceTypes = computed(() => resources.value.map((item) => item.type).join(' / '))
</script>

<template>
  <section class="page">
    <h1 class="page-title">个性化资源详情</h1>
    <p class="page-copy">
      展示后端生成的 5 类学习资源，并为每个资源呈现来源依据与审校报告。
    </p>

    <div v-if="!packageResult" class="panel empty-panel">
      <el-empty description="还没有可展示的资源包">
        <el-button type="primary" @click="router.push('/')">先生成资源包</el-button>
      </el-empty>
    </div>

    <template v-else>
      <div class="resource-summary">
        <div>
          <span>task_id</span>
          <strong>{{ packageResult.task_id }}</strong>
        </div>
        <div>
          <span>资源类型</span>
          <strong>{{ resourceTypes }}</strong>
        </div>
      </div>

      <div class="resource-stack">
        <ResourceCard
          v-for="resource in resources"
          :key="resource.resource_id || `${resource.type}-${resource.title}`"
          :resource="resource"
        />
      </div>
    </template>
  </section>
</template>

<style scoped>
.empty-panel {
  margin-top: 36px;
}

.resource-summary {
  display: grid;
  grid-template-columns: minmax(240px, 0.8fr) minmax(0, 1.2fr);
  gap: 16px;
  margin-top: 36px;
}

.resource-summary div {
  padding: 22px;
  border: 1px solid rgba(16, 24, 40, 0.08);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.86);
  box-shadow: 0 20px 56px rgba(31, 41, 55, 0.08);
}

.resource-summary span {
  display: block;
  margin-bottom: 10px;
  color: #667085;
  font-size: 14px;
}

.resource-summary strong {
  display: block;
  color: #101828;
  font-size: 20px;
  line-height: 1.45;
  word-break: break-word;
}

.resource-stack {
  display: grid;
  gap: 28px;
  margin-top: 28px;
}

@media (max-width: 760px) {
  .resource-summary {
    grid-template-columns: 1fr;
  }
}
</style>
