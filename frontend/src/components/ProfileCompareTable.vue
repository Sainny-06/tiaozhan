<script setup lang="ts">
import type { ProfileDiffItem } from '../types/quiz'

defineProps<{
  diffs: ProfileDiffItem[]
}>()

function formatValue(value: unknown) {
  if (Array.isArray(value)) {
    return value.join('、')
  }
  if (value && typeof value === 'object') {
    return JSON.stringify(value, null, 2)
  }
  return String(value ?? '未评估')
}
</script>

<template>
  <el-empty v-if="!diffs.length" description="暂无画像变化" />
  <el-table v-else :data="diffs" border class="profile-compare-table">
    <el-table-column prop="field" label="画像维度" min-width="160" />
    <el-table-column label="更新前" min-width="180">
      <template #default="{ row }">
        <span>{{ formatValue(row.before) }}</span>
      </template>
    </el-table-column>
    <el-table-column label="更新后" min-width="180">
      <template #default="{ row }">
        <span>{{ formatValue(row.after) }}</span>
      </template>
    </el-table-column>
    <el-table-column prop="reason" label="变化原因" min-width="220" />
  </el-table>
</template>

<style scoped>
.profile-compare-table {
  width: 100%;
}
</style>
