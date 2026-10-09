<script setup lang="ts">
import { computed } from 'vue'
import { Right } from '@element-plus/icons-vue'
import { vLoading } from 'element-plus'

import { plainText } from '../markdown'
import { formatDate } from '../time'
import type { Note } from '@/shared/types'

const props = defineProps<{ notes: Note[]; loading: boolean }>()
const emit = defineEmits<{ open: [Note] }>()

// 摘要只算一次（正则不便宜，模板里重复调用会白跑）
const rows = computed(() => props.notes.map((note) => ({ note, excerpt: plainText(note.content) })))
</script>

<template>
  <div class="panel">
    <div v-loading="loading" class="rows">
      <button
        v-for="row in rows"
        :key="row.note.id"
        type="button"
        class="row"
        @click="emit('open', row.note)"
      >
        <span class="body">
          <span class="title">{{ row.note.title }}</span>
          <span v-if="row.excerpt" class="excerpt">{{ row.excerpt }}</span>
        </span>

        <span class="meta">
          <span class="when">{{ formatDate(row.note.updated_at) }}</span>
          <el-icon class="arrow"><Right /></el-icon>
        </span>
      </button>

      <p v-if="!loading && !notes.length" class="empty">还没有文章，点右上角「写一篇」开始</p>
    </div>
  </div>
</template>

<style scoped>
.rows {
  min-height: 96px;
}

/* 两行式：标题 + 摘要，右侧日期；留白给足，别挤在一起 */
.row {
  display: flex;
  align-items: center;
  gap: 22px;
  width: 100%;
  padding: 18px 24px;
  border: none;
  border-bottom: 1px solid var(--warm-line-soft);
  background: transparent;
  font: inherit;
  text-align: left;
  cursor: pointer;
  transition: background 0.18s ease;
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

.body {
  display: flex;
  flex: 1;
  min-width: 0;
  flex-direction: column;
  gap: 7px;
}

.title {
  overflow: hidden;
  color: var(--ink-900);
  font-size: 16px;
  font-weight: 600;
  line-height: 1.5;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.excerpt {
  overflow: hidden;
  color: var(--ink-500);
  font-size: 13px;
  line-height: 1.6;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.meta {
  display: flex;
  flex-shrink: 0;
  align-items: center;
  gap: 12px;
}

.when {
  color: var(--ink-400);
  font-size: 12.5px;
  white-space: nowrap;
}

.arrow {
  color: var(--honey-300);
  opacity: 0;
  transform: translateX(-4px);
  transition:
    opacity 0.18s ease,
    transform 0.18s ease;
}

.row:hover .arrow {
  opacity: 1;
  transform: translateX(0);
}

.empty {
  margin: 0;
  padding: 40px 32px;
  color: var(--ink-400);
  font-size: 13px;
  text-align: center;
}
</style>
