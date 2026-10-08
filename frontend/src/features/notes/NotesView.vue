<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { listNotes } from './api'
import ArticleList from './components/ArticleList.vue'
import QuickNoteDialog from './components/QuickNoteDialog.vue'
import QuickNoteList from './components/QuickNoteList.vue'
import type { Note, NoteKind } from '@/shared/types'

const route = useRoute()
const router = useRouter()

const tab = ref<NoteKind>(route.query.tab === 'article' ? 'article' : 'quick')
const notes = ref<Note[]>([])
const total = ref(0)
const page = ref(1)
const size = 10
const loading = ref(false)

const dialogVisible = ref(false)
const editing = ref<Note | null>(null)

async function load() {
  loading.value = true
  try {
    const data = await listNotes({ kind: tab.value, page: page.value, size })
    notes.value = data.items
    total.value = data.total
  } finally {
    loading.value = false
  }
}

function onTabChange(value: string | number | boolean | undefined) {
  tab.value = value === 'article' ? 'article' : 'quick'
  page.value = 1
  void router.replace({ query: { ...route.query, tab: tab.value } })
  void load()
}

function onCreate() {
  if (tab.value === 'quick') {
    editing.value = null
    dialogVisible.value = true
  } else {
    void router.push('/notes/articles/new')
  }
}

function onEditQuick(note: Note) {
  editing.value = note
  dialogVisible.value = true
}

function onOpenArticle(note: Note) {
  void router.push(`/notes/articles/${note.id}`)
}

onMounted(load)
</script>

<template>
  <div>
    <div class="page-head">
      <div>
        <h2 class="page-title">笔记</h2>
        <p class="page-sub">
          {{ tab === 'quick' ? '随手记下的小问题、心得' : '写完整的东西' }} · 共 {{ total }} 条
        </p>
      </div>
      <el-button type="primary" @click="onCreate">
        {{ tab === 'quick' ? '写一条' : '写一篇' }}
      </el-button>
    </div>

    <el-radio-group :model-value="tab" class="switcher" @change="onTabChange">
      <el-radio-button value="quick">随手小记</el-radio-button>
      <el-radio-button value="article">文章</el-radio-button>
    </el-radio-group>

    <QuickNoteList
      v-if="tab === 'quick'"
      :notes="notes"
      :loading="loading"
      @edit="onEditQuick"
      @removed="load"
    />
    <ArticleList v-else :notes="notes" :loading="loading" @open="onOpenArticle" />

    <el-pagination
      v-if="total > size"
      v-model:current-page="page"
      class="pager"
      layout="prev, pager, next"
      :total="total"
      :page-size="size"
      @current-change="load"
    />

    <QuickNoteDialog v-model="dialogVisible" :note="editing" @saved="load" />
  </div>
</template>

<style scoped>
.switcher {
  margin-bottom: 18px;
}

.pager {
  justify-content: flex-end;
  margin-top: 18px;
}
</style>
