<script setup lang="ts">
import type { ReviewReport } from '../types/package'

defineProps<{
  reviewReport: ReviewReport
}>()

const labels: Record<keyof ReviewReport, string> = {
  knowledge_grounding: '知识库引用',
  difficulty_match: '难度匹配',
  answer_consistency: '答案一致性',
  content_safety: '内容安全',
  comment: '审校说明',
}
</script>

<template>
  <section class="resource-section">
    <h3>审校报告</h3>
    <div class="review-grid">
      <div
        v-for="key in ['knowledge_grounding', 'difficulty_match', 'answer_consistency', 'content_safety']"
        :key="key"
        class="review-item"
      >
        <span>{{ labels[key as keyof ReviewReport] }}</span>
        <strong>{{ reviewReport[key as keyof ReviewReport] }}</strong>
      </div>
    </div>
    <p class="review-comment">{{ reviewReport.comment }}</p>
  </section>
</template>

<style scoped>
.review-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 10px;
}

.review-item {
  padding: 14px;
  border-radius: 8px;
  background: #f3f7f4;
}

.review-item span {
  display: block;
  margin-bottom: 6px;
  color: #667085;
  font-size: 13px;
}

.review-item strong {
  color: #147a3f;
}

.review-comment {
  margin: 14px 0 0;
  color: #475467;
  line-height: 1.7;
}

@media (max-width: 860px) {
  .review-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}
</style>
