<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

import { loadRecentPackage } from '../api/packageStore'
import type { AgentOutput, PackageGenerateResponse } from '../types/package'

const router = useRouter()
const packageResult = ref<PackageGenerateResponse | null>(loadRecentPackage())

const agentPanels = computed<Array<{ name: string; output: AgentOutput }>>(() => {
  if (!packageResult.value) {
    return []
  }

  return [
    {
      name: 'ProfileAgent',
      output: packageResult.value.profile_agent_output,
    },
    {
      name: 'RetrievalAgent',
      output: packageResult.value.retrieval_agent_output,
    },
    {
      name: 'ResourceAgent',
      output: packageResult.value.resource_agent_output,
    },
    {
      name: 'ReviewPathAgent',
      output: packageResult.value.review_path_agent_output,
    },
  ]
})

const resourceCount = computed(() => packageResult.value?.resources.length ?? 0)
const learningPathCount = computed(() => packageResult.value?.learning_path.length ?? 0)

function formatOutput(output: AgentOutput) {
  return JSON.stringify(output, null, 2)
}
</script>

<template>
  <section class="page">
    <h1 class="page-title">真实 Agent 流程输出</h1>
    <p class="page-copy">
      这里展示最近一次资源包生成结果。所有 Agent 日志均来自后端返回，不在前端伪造。
    </p>

    <div v-if="!packageResult" class="panel empty-panel">
      <el-empty description="还没有资源包结果">
        <el-button type="primary" @click="router.push('/')">返回画像输入</el-button>
      </el-empty>
    </div>

    <template v-else>
      <div class="summary-grid">
        <div class="summary-card">
          <span>task_id</span>
          <strong>{{ packageResult.task_id }}</strong>
        </div>
        <div class="summary-card">
          <span>资源数量</span>
          <strong>{{ resourceCount }}</strong>
        </div>
        <div class="summary-card">
          <span>学习路径步骤</span>
          <strong>{{ learningPathCount }}</strong>
        </div>
      </div>

      <div class="panel">
        <el-collapse class="agent-collapse" :model-value="agentPanels.map((item) => item.name)">
          <el-collapse-item v-for="panel in agentPanels" :key="panel.name" :name="panel.name">
            <template #title>
              <div class="agent-title">
                <span>{{ panel.name }}</span>
                <small>{{ panel.output.agent_log }}</small>
              </div>
            </template>

            <div class="agent-body">
              <div class="agent-log">
                <strong>后端日志</strong>
                <p>{{ panel.output.agent_log }}</p>
              </div>
              <pre class="result-box">{{ formatOutput(panel.output) }}</pre>
            </div>
          </el-collapse-item>
        </el-collapse>
      </div>

      <div class="panel">
        <h2 class="section-title">资源与路径摘要</h2>
        <ul class="resource-list">
          <li v-for="resource in packageResult.resources" :key="resource.resource_id || resource.title">
            <strong>{{ resource.title }}</strong>
            <span>{{ resource.type }}</span>
          </li>
        </ul>
      </div>
    </template>
  </section>
</template>

<style scoped>
.summary-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.7fr) repeat(2, minmax(160px, 0.65fr));
  gap: 16px;
  margin-top: 36px;
}

.summary-card {
  min-height: 112px;
  padding: 22px;
  border: 1px solid rgba(16, 24, 40, 0.08);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.86);
  box-shadow: 0 20px 56px rgba(31, 41, 55, 0.08);
}

.summary-card span {
  display: block;
  margin-bottom: 10px;
  color: #667085;
  font-size: 14px;
}

.summary-card strong {
  display: block;
  color: #101828;
  font-size: clamp(24px, 3vw, 36px);
  line-height: 1.15;
  word-break: break-all;
}

.agent-collapse {
  border: 0;
}

.agent-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
  width: 100%;
  padding-right: 16px;
}

.agent-title span {
  color: #101828;
  font-weight: 800;
}

.agent-title small {
  overflow: hidden;
  color: #667085;
  font-size: 13px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.agent-body {
  display: grid;
  gap: 16px;
  padding: 4px 0 18px;
}

.agent-log {
  padding: 16px;
  border-radius: 8px;
  background: #f3f6fb;
}

.agent-log p {
  margin: 8px 0 0;
  color: #475467;
}

.section-title {
  margin: 0 0 18px;
  color: #101828;
  font-size: 24px;
}

.resource-list {
  display: grid;
  gap: 12px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.resource-list li {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 14px 0;
  border-bottom: 1px solid rgba(16, 24, 40, 0.08);
}

.resource-list span {
  padding: 6px 10px;
  border-radius: 999px;
  background: #edf3ff;
  color: #2f5fb8;
  font-size: 13px;
}

.empty-panel {
  margin-top: 36px;
}

@media (max-width: 860px) {
  .summary-grid {
    grid-template-columns: 1fr;
  }

  .agent-title {
    align-items: flex-start;
    flex-direction: column;
    gap: 4px;
  }
}
</style>
