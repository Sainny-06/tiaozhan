<script setup lang="ts">
import MermaidViewer from './MermaidViewer.vue'

defineProps<{
  title: string
  steps?: string[]
  mermaidCode?: string
}>()
</script>

<template>
  <div class="animation-demo">
    <div v-if="steps?.length" class="step-track">
      <div v-for="(step, index) in steps" :key="`${step}-${index}`" class="step-node">
        <span>{{ index + 1 }}</span>
        <strong>{{ step }}</strong>
      </div>
    </div>

    <MermaidViewer v-if="mermaidCode" :code="mermaidCode" />
  </div>
</template>

<style scoped>
.animation-demo {
  display: grid;
  gap: 20px;
}

.step-track {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  gap: 12px;
}

.step-node {
  position: relative;
  min-height: 96px;
  padding: 16px;
  overflow: hidden;
  border-radius: 8px;
  background: linear-gradient(145deg, #10233f, #1e5a70);
  color: #ffffff;
}

.step-node::after {
  position: absolute;
  inset: auto -20px -30px auto;
  width: 90px;
  height: 90px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.14);
  content: "";
}

.step-node span {
  display: inline-grid;
  place-items: center;
  width: 28px;
  height: 28px;
  margin-bottom: 12px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.18);
  font-weight: 800;
}

.step-node strong {
  display: block;
  line-height: 1.5;
}
</style>
