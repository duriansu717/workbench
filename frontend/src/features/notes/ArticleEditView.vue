<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft } from '@element-plus/icons-vue'
import { ElMessage, vLoading } from 'element-plus'

import { createNote, getNote, updateNote } from './api'
import NoteEditor from './components/NoteEditor.vue'

const route = useRoute()
const router = useRouter()

const id = computed(() => (route.params.id ? String(route.params.id) : null))
const loading = ref(false)
const saving = ref(false)

const title = ref('')
const content = ref('')

onMounted(async () => {
  if (!id.value) return
  loading.value = true
  try {
    const note = await getNote(id.value)
    title.value = note.title ?? ''
    content.value = note.content ?? ''
  } finally {
    loading.value = false
  }
})

async function save() {
  if (!title.value.trim()) {
    ElMessage.warning('文章要有标题')
    return
  }
  saving.value = true
  try {
    if (id.value) {
      await updateNote(id.value, { title: title.value, content: content.value })
      ElMessage.success('已保存')
      void router.push(`/notes/articles/${id.value}`)
    } else {
      const created = await createNote({
        kind: 'article',
        title: title.value,
        content: content.value,
      })
      ElMessage.success('已创建')
      void router.replace(`/notes/articles/${created.id}`)
    }
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div v-loading="loading">
    <div class="bar">
      <el-button link @click="router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <el-button type="primary" :loading="saving" @click="save">
        {{ id ? '保存' : '创建' }}
      </el-button>
    </div>

    <div class="panel editor-panel">
      <input v-model="title" class="title-input" maxlength="200" placeholder="标题" />
      <NoteEditor
        v-model="content"
        mode="article"
        placeholder="正文…（Ctrl+S 保存）"
        @save="save"
      />
    </div>
  </div>
</template>

<style scoped>
.bar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}

.editor-panel {
  padding: 20px 22px 22px;
}

.title-input {
  width: 100%;
  margin-bottom: 14px;
  padding: 4px 2px 10px;
  border: none;
  border-bottom: 1px solid var(--warm-line-soft);
  background: transparent;
  color: var(--ink-900);
  font-family: inherit;
  font-size: 22px;
  font-weight: 700;
  outline: none;
  transition: border-color 0.16s ease;
}

.title-input::placeholder {
  color: var(--ink-400);
  font-weight: 500;
}

.title-input:focus {
  border-bottom-color: var(--honey-500);
}
</style>
