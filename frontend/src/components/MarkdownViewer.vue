<script setup lang="ts">
import MarkdownIt from 'markdown-it'
import { computed } from 'vue'

const props = defineProps<{
  content: string
}>()

const markdown = new MarkdownIt({
  html: false,
  linkify: true,
  breaks: true,
})

const rendered = computed(() => markdown.render(props.content || ''))
</script>

<template>
  <article class="markdown-viewer" v-html="rendered" />
</template>

<style scoped>
.markdown-viewer {
  color: #344054;
  line-height: 1.85;
}

.markdown-viewer :deep(h1),
.markdown-viewer :deep(h2),
.markdown-viewer :deep(h3) {
  margin: 18px 0 10px;
  color: #101828;
}

.markdown-viewer :deep(p) {
  margin: 0 0 12px;
}

.markdown-viewer :deep(code) {
  padding: 2px 5px;
  border-radius: 5px;
  background: #edf2f7;
  color: #1d2939;
}
</style>
