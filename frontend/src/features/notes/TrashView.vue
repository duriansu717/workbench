<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox, vLoading } from 'element-plus'

import { listDeletedNotes, purgeNote, restoreNote } from './api'
import { formatDateTime } from './time'
import type { Note } from '@/shared/types'

const router = useRouter()
const notes = ref<Note[]>([])
const loading = ref(false)

async function load() {
  loading.value = true
  try {
    // 回收站不做分页（个人使用量级，直接列全）
    notes.value = (await listDeletedNotes({ page: 1, size: 100 })).items
  } finally {
    loading.value = false
  }
}

async function onRestore(note: Note) {
  await restoreNote(note.id)
  ElMessage.success('已恢复')
  await load()
}

async function onPurge(note: Note) {
  await ElMessageBox.confirm('彻底删除后无法恢复，确定吗？', '彻底删除', {
    type: 'warning',
    confirmButtonText: '彻底删除',
    cancelButtonText: '再想想',
  })
  await purgeNote(note.id)
  ElMessage.success('已彻底删除')
  await load()
}

onMounted(load)
</script>

<template>
  <div>
    <div class="page-head">
      <div>
        <h2 class="page-title">回收站</h2>
        <p class="page-sub">这里的笔记已从列表隐藏，数据还在 —— 可以恢复，也可以彻底删除</p>
      </div>
      <el-button link @click="router.push('/notes')">
        <el-icon><ArrowLeft /></el-icon>
        返回笔记
      </el-button>
    </div>

    <div class="panel">
      <div v-loading="loading" class="rows">
        <div v-for="note in notes" :key="note.id" class="row">
          <span class="tag">{{ note.kind === 'quick' ? '小记' : '文章' }}</span>
          <span class="main">
            <span class="title">{{
              note.title || (note.content ?? '').slice(0, 60) || '（空内容）'
            }}</span>
            <span class="when">
              删除于 {{ note.deleted_at ? formatDateTime(note.deleted_at) : '—' }}
            </span>
          </span>
          <span class="ops">
            <el-button link type="primary" @click="onRestore(note)">恢复</el-button>
            <el-button link type="danger" @click="onPurge(note)">彻底删除</el-button>
          </span>
        </div>

        <p v-if="!loading && !notes.length" class="empty">回收站是空的</p>
      </div>
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
  padding: 14px 20px;
  border-bottom: 1px solid var(--warm-line-soft);
}

.row:last-of-type {
  border-bottom: none;
}

.tag {
  flex-shrink: 0;
  padding: 2px 8px;
  border-radius: 8px;
  background: var(--honey-50);
  color: var(--honey-700);
  font-size: 12px;
}

.main {
  display: flex;
  flex: 1;
  min-width: 0;
  flex-direction: column;
  gap: 3px;
}

.title {
  overflow: hidden;
  color: var(--ink-700);
  font-size: 14.5px;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.when {
  color: var(--ink-400);
  font-size: 12px;
}

.ops {
  flex-shrink: 0;
}

.empty {
  margin: 0;
  padding: 32px;
  color: var(--ink-400);
  font-size: 13px;
  text-align: center;
}
</style>
