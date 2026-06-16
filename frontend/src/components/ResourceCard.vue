<script setup lang="ts">
import AnimationDemo from './AnimationDemo.vue'
import MarkdownViewer from './MarkdownViewer.vue'
import MermaidViewer from './MermaidViewer.vue'
import ReviewReportPanel from './ReviewReportPanel.vue'
import SourceRefsPanel from './SourceRefsPanel.vue'
import type { LearningResource } from '../types/package'

defineProps<{
  resource: LearningResource
}>()

function resourceTypeLabel(type: string) {
  const labels: Record<string, string> = {
    lecture: '个性化讲义',
    mindmap: '思维导图',
    quiz: '分层题库',
    code_lab: '代码实操',
    animation: '图解演示',
  }
  return labels[type] ?? type
}

function optionEntries(options: unknown) {
  if (!options || typeof options !== 'object') {
    return []
  }
  return Object.entries(options as Record<string, string>)
}
</script>

<template>
  <article class="resource-card">
    <header class="resource-header">
      <div>
        <span class="resource-type">{{ resourceTypeLabel(resource.type) }}</span>
        <h2>{{ resource.title }}</h2>
      </div>
    </header>

    <section class="resource-section">
      <h3>个性化说明</h3>
      <p>
        该资源基于学生画像、目标主题和 RetrievalAgent 返回的知识库来源生成，适配当前学习基础与资源偏好。
      </p>
    </section>

    <section class="resource-section">
      <h3>资源内容</h3>

      <MarkdownViewer
        v-if="resource.type === 'lecture'"
        :content="resource.content || '暂无讲义内容。'"
      />

      <MermaidViewer
        v-else-if="resource.type === 'mindmap' && resource.mermaid_code"
        :code="resource.mermaid_code"
      />

      <div v-else-if="resource.type === 'quiz'" class="quiz-list">
        <article
          v-for="(question, index) in resource.questions || []"
          :key="String(question.question_id || index)"
          class="quiz-item"
        >
          <div class="quiz-meta">
            <span>{{ question.knowledge_point }}</span>
            <span>{{ question.difficulty }}</span>
          </div>
          <h4>{{ index + 1 }}. {{ question.question }}</h4>
          <ul>
            <li v-for="[key, value] in optionEntries(question.options)" :key="key">
              <strong>{{ key }}</strong>
              <span>{{ value }}</span>
            </li>
          </ul>
        </article>
      </div>

      <pre v-else-if="resource.type === 'code_lab'" class="code-block"><code>{{ resource.code }}</code></pre>

      <AnimationDemo
        v-else-if="resource.type === 'animation'"
        :title="resource.title"
        :steps="resource.steps"
        :mermaid-code="resource.mermaid_code"
      />

      <MarkdownViewer v-else :content="resource.content || '暂无可展示内容。'" />
    </section>

    <SourceRefsPanel :source-refs="resource.source_refs || []" />
    <ReviewReportPanel :review-report="resource.review_report" />
  </article>
</template>

<style scoped>
.resource-card {
  display: grid;
  gap: 24px;
  padding: 28px;
  border: 1px solid rgba(16, 24, 40, 0.08);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 24px 70px rgba(31, 41, 55, 0.10);
}

.resource-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 18px;
}

.resource-type {
  display: inline-flex;
  margin-bottom: 10px;
  padding: 6px 10px;
  border-radius: 999px;
  background: #17202a;
  color: #ffffff;
  font-size: 13px;
}

.resource-header h2 {
  margin: 0;
  color: #101828;
  font-size: clamp(24px, 3vw, 36px);
  line-height: 1.2;
}

.resource-section {
  display: grid;
  gap: 12px;
}

.resource-section h3 {
  margin: 0;
  color: #101828;
  font-size: 18px;
}

.resource-section p {
  margin: 0;
  color: #475467;
  line-height: 1.8;
}

.quiz-list {
  display: grid;
  gap: 14px;
}

.quiz-item {
  padding: 18px;
  border: 1px solid rgba(16, 24, 40, 0.08);
  border-radius: 8px;
  background: #f8fbff;
}

.quiz-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 10px;
}

.quiz-meta span {
  padding: 5px 9px;
  border-radius: 999px;
  background: #edf3ff;
  color: #2f5fb8;
  font-size: 12px;
}

.quiz-item h4 {
  margin: 0 0 12px;
  color: #101828;
  font-size: 17px;
  line-height: 1.6;
}

.quiz-item ul {
  display: grid;
  gap: 8px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.quiz-item li {
  display: flex;
  gap: 10px;
  color: #475467;
}

.quiz-item li strong {
  color: #101828;
}

.code-block {
  overflow-x: auto;
  margin: 0;
  padding: 18px;
  border-radius: 8px;
  background: #101828;
  color: #e6edf7;
  line-height: 1.7;
}
</style>
