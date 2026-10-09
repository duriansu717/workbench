<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox, vLoading } from 'element-plus'

import { getNote, removeNote } from './api'
import NoteContent from './components/NoteContent.vue'
import { formatDateTime } from './time'
import type { Note } from '@/shared/types'

const route = useRoute()
const router = useRouter()

const note = ref<Note | null>(null)
const loading = ref(true)

onMounted(async () => {
  try {
    note.value = await getNote(String(route.params.id))
  } finally {
    loading.value = false
  }
})

async function onRemove() {
  if (!note.value) return
  await ElMessageBox.confirm(`删除「${note.value.title}」？删了就找不回来了。`, '删除确认', {
    type: 'warning',
  })
  await removeNote(note.value.id)
  ElMessage.success('已删除')
  void router.replace({ path: '/notes', query: { tab: 'article' } })
}
</script>

<template>
  <div v-loading="loading">
    <div class="bar">
      <el-button link @click="router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <div v-if="note" class="ops">
        <el-button link type="primary" @click="router.push(`/notes/articles/${note.id}/edit`)">
          编辑
        </el-button>
        <el-button link type="danger" @click="onRemove">删除</el-button>
      </div>
    </div>

    <article v-if="note" class="panel article">
      <h1 class="title">{{ note.title }}</h1>
      <p class="meta">
        创建于 {{ formatDateTime(note.created_at) }} · 更新于 {{ formatDateTime(note.updated_at) }}
      </p>
      <div class="rule" />
      <NoteContent :content="note.content" />
    </article>
  </div>
</template>

<style scoped>
.bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

/* 正文栏收窄到 860px：长文更好读，图片也不会被拉到整屏宽 */
.article {
  max-width: 860px;
  margin: 0 auto;
  padding: 32px 38px 40px;
}

.title {
  margin: 0;
  color: var(--ink-900);
  font-size: 26px;
  line-height: 1.4;
}

.meta {
  margin: 10px 0 0;
  color: var(--ink-400);
  font-size: 12.5px;
}

.rule {
  height: 1px;
  margin: 20px 0 6px;
  background: var(--warm-line-soft);
}
</style>
