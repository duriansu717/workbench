<script setup lang="ts">
import { Right } from '@element-plus/icons-vue'
import { vLoading } from 'element-plus'

import { formatDateTime } from '../time'
import type { Note } from '@/shared/types'

defineProps<{ notes: Note[]; loading: boolean }>()
const emit = defineEmits<{ open: [Note] }>()
</script>

<template>
  <div class="panel">
    <div v-loading="loading" class="rows">
      <button
        v-for="article in notes"
        :key="article.id"
        type="button"
        class="row"
        @click="emit('open', article)"
      >
        <span class="title">{{ article.title }}</span>
        <span class="when">{{ formatDateTime(article.updated_at) }}</span>
        <el-icon class="arrow"><Right /></el-icon>
      </button>

      <p v-if="!loading && !notes.length" class="empty">还没有文章，点右上角「写一篇」开始</p>
    </div>
  </div>
</template>

<style scoped>
.rows {
  min-height: 80px;
}

.row {
  display: flex;
  align-items: center;
  gap: 14px;
  width: 100%;
  padding: 15px 20px;
  border: none;
  border-bottom: 1px solid var(--warm-line-soft);
  background: transparent;
  font: inherit;
  text-align: left;
  cursor: pointer;
  transition: background 0.16s ease;
}

.row:last-of-type {
  border-bottom: none;
}

.row:hover {
  background: var(--warm-surface-warm);
}

.row:focus-visible {
  outline: 2px solid var(--honey-500);
  outline-offset: -2px;
}

.title {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  color: var(--ink-900);
  font-size: 15px;
  font-weight: 600;
}

.when {
  flex-shrink: 0;
  color: var(--ink-400);
  font-size: 12.5px;
}

.arrow {
  flex-shrink: 0;
  color: var(--honey-300);
  opacity: 0;
  transform: translateX(-4px);
  transition:
    opacity 0.16s ease,
    transform 0.16s ease;
}

.row:hover .arrow {
  opacity: 1;
  transform: translateX(0);
}

.empty {
  margin: 0;
  padding: 32px;
  color: var(--ink-400);
  font-size: 13px;
  text-align: center;
}
</style>
