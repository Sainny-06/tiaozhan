<script setup lang="ts">
import type { SourceRef } from '../types/package'

defineProps<{
  sourceRefs: SourceRef[]
}>()
</script>

<template>
  <section class="resource-section">
    <h3>来源依据</h3>
    <el-empty v-if="!sourceRefs.length" description="暂无来源依据" />
    <ul v-else class="source-list">
      <li v-for="(ref, index) in sourceRefs" :key="`${ref.file}-${ref.section}-${index}`">
        <div>
          <strong>{{ ref.file }}</strong>
          <span>{{ ref.section }}</span>
        </div>
        <p>{{ ref.reason || '该片段用于支撑当前资源内容生成。' }}</p>
      </li>
    </ul>
  </section>
</template>

<style scoped>
.source-list {
  display: grid;
  gap: 12px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.source-list li {
  padding: 14px;
  border: 1px solid rgba(16, 24, 40, 0.08);
  border-radius: 8px;
  background: #f8fbff;
}

.source-list div {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
}

.source-list strong {
  color: #101828;
}

.source-list span {
  padding: 4px 8px;
  border-radius: 999px;
  background: #edf3ff;
  color: #2f5fb8;
  font-size: 12px;
}

.source-list p {
  margin: 8px 0 0;
  color: #667085;
  line-height: 1.7;
}
</style>
