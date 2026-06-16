<script setup lang="ts">
import mermaid from 'mermaid'
import { computed, nextTick, onMounted, ref, watch } from 'vue'

const props = defineProps<{
  code: string
}>()

const containerId = `mermaid-${Math.random().toString(36).slice(2)}`
const svg = ref('')
const error = ref('')

const normalizedCode = computed(() => props.code?.trim() || '')

async function renderMermaid() {
  error.value = ''
  svg.value = ''

  if (!normalizedCode.value) {
    return
  }

  try {
    await nextTick()
    const result = await mermaid.render(containerId, normalizedCode.value)
    svg.value = result.svg
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Mermaid 渲染失败'
  }
}

mermaid.initialize({
  startOnLoad: false,
  securityLevel: 'strict',
  theme: 'default',
})

onMounted(renderMermaid)
watch(() => props.code, renderMermaid)
</script>

<template>
  <div class="mermaid-viewer">
    <div v-if="svg" class="mermaid-canvas" v-html="svg" />
    <pre v-else class="code-fallback">{{ normalizedCode }}</pre>
    <el-alert
      v-if="error"
      class="mermaid-error"
      type="warning"
      title="Mermaid 渲染失败，已展示原始代码"
      :description="error"
      :closable="false"
      show-icon
    />
  </div>
</template>

<style scoped>
.mermaid-viewer {
  display: grid;
  gap: 12px;
}

.mermaid-canvas {
  overflow-x: auto;
  padding: 18px;
  border-radius: 8px;
  background: #ffffff;
}

.mermaid-canvas :deep(svg) {
  max-width: 100%;
  height: auto;
}

.code-fallback {
  overflow-x: auto;
  margin: 0;
  padding: 18px;
  border-radius: 8px;
  background: #101828;
  color: #e6edf7;
  line-height: 1.7;
}

.mermaid-error {
  margin-top: 4px;
}
</style>
