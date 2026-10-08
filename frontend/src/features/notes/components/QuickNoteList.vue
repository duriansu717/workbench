<script setup lang="ts">
import { ElMessage, ElMessageBox, vLoading } from 'element-plus'

import { removeNote } from '../api'
import { formatRelative } from '../time'
import NoteContent from './NoteContent.vue'
import type { Note } from '@/shared/types'

defineProps<{ notes: Note[]; loading: boolean }>()
const emit = defineEmits<{ edit: [Note]; removed: [] }>()

async function onRemove(note: Note) {
  await ElMessageBox.confirm('删除这条小记？删了就找不回来了。', '删除确认', { type: 'warning' })
  await removeNote(note.id)
  ElMessage.success('已删除')
  emit('removed')
}
</script>

<template>
  <div v-loading="loading" class="timeline">
    <article v-for="note in notes" :key="note.id" class="entry">
      <div class="rail"><span class="dot" /></div>

      <div class="card">
        <header class="head">
          <time class="when">{{ formatRelative(note.created_at) }}</time>
          <span class="ops">
            <el-button link type="primary" @click="emit('edit', note)">编辑</el-button>
            <el-button link type="danger" @click="onRemove(note)">删除</el-button>
          </span>
        </header>
        <NoteContent :content="note.content" compact />
      </div>
    </article>

    <p v-if="!loading && !notes.length" class="empty">还没有小记，点右上角「写一条」记一笔</p>
  </div>
</template>

<style scoped>
.timeline {
  min-height: 80px;
}

.entry {
  display: flex;
  gap: 0;
}

/* 左侧时间轴：一条竖线 + 一个暖色圆点 */
.rail {
  position: relative;
  width: 26px;
  flex-shrink: 0;
}

.rail::before {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  left: 12px;
  width: 1px;
  background: var(--warm-line);
}

.entry:first-child .rail::before {
  top: 22px;
}

.entry:last-child .rail::before {
  bottom: -6px;
}

.dot {
  position: absolute;
  top: 18px;
  left: 8px;
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--honey-300);
  box-shadow: 0 0 0 3px rgba(247, 200, 120, 0.25);
}

.card {
  flex: 1;
  min-width: 0;
  margin: 0 0 12px 8px;
  padding: 14px 18px 16px;
  border: 1px solid var(--warm-line-soft);
  border-radius: var(--warm-radius);
  background: var(--warm-surface-warm);
  box-shadow: var(--warm-shadow-sm);
  transition:
    box-shadow 0.18s ease,
    transform 0.18s ease;
}

.card:hover {
  transform: translateY(-1px);
  box-shadow: var(--warm-shadow-md);
}

.head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 6px;
}

.when {
  color: var(--ink-400);
  font-size: 12.5px;
}

.ops {
  opacity: 0;
  transition: opacity 0.16s ease;
}

.card:hover .ops,
.card:focus-within .ops {
  opacity: 1;
}

.empty {
  margin: 0;
  padding: 32px;
  border: 1px dashed var(--warm-line);
  border-radius: var(--warm-radius);
  color: var(--ink-400);
  font-size: 13px;
  text-align: center;
}
</style>
