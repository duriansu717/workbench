<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'

import { api } from '@/shared/api'
import type { Note, Page } from '@/shared/types'

const loading = ref(false)
const notes = ref<Note[]>([])
const total = ref(0)
const page = ref(1)
const size = ref(10)

const dialogVisible = ref(false)
const editingId = ref<string | null>(null)
const form = reactive({ title: '', content: '' })

async function load() {
  loading.value = true
  try {
    const { data } = await api.get<Page<Note>>('/notes', {
      params: { page: page.value, size: size.value },
    })
    notes.value = data.items
    total.value = data.total
  } finally {
    loading.value = false
  }
}

function openCreate() {
  editingId.value = null
  form.title = ''
  form.content = ''
  dialogVisible.value = true
}

function openEdit(note: Note) {
  editingId.value = note.id
  form.title = note.title
  form.content = note.content ?? ''
  dialogVisible.value = true
}

async function save() {
  if (!form.title.trim()) {
    ElMessage.warning('标题不能为空')
    return
  }
  const payload = { title: form.title, content: form.content }
  if (editingId.value) {
    await api.patch(`/notes/${editingId.value}`, payload)
    ElMessage.success('已保存')
  } else {
    await api.post('/notes', payload)
    ElMessage.success('已创建')
  }
  dialogVisible.value = false
  await load()
}

async function remove(note: Note) {
  await ElMessageBox.confirm(`确定删除「${note.title}」吗？`, '删除确认', { type: 'warning' })
  await api.delete(`/notes/${note.id}`)
  ElMessage.success('已删除')
  await load()
}

onMounted(load)
</script>

<template>
  <div>
    <div class="page-head">
      <div>
        <h2 class="page-title">笔记</h2>
        <p class="page-sub">随手记下一点什么，一共 {{ total }} 条</p>
      </div>
      <el-button type="primary" @click="openCreate">新建笔记</el-button>
    </div>

    <div class="panel">
      <el-table
        v-loading="loading"
        :data="notes"
        empty-text="还没有笔记，点右上角「新建笔记」写一条吧 ✍️"
        style="width: 100%"
      >
        <el-table-column prop="title" label="标题" min-width="180" />
        <el-table-column prop="content" label="内容" min-width="260" show-overflow-tooltip />
        <el-table-column label="创建时间" width="190">
          <template #default="{ row }">
            <span class="time">{{ new Date(row.created_at).toLocaleString() }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="140" align="right">
          <template #default="{ row }">
            <!-- el-table 插槽的 row 是宽松类型（DefaultRow），这里断言成业务类型 -->
            <el-button link type="primary" @click="openEdit(row as Note)">编辑</el-button>
            <el-button link type="danger" @click="remove(row as Note)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-pagination
      v-model:current-page="page"
      class="pager"
      layout="prev, pager, next, total"
      :total="total"
      :page-size="size"
      @current-change="load"
    />

    <el-dialog v-model="dialogVisible" :title="editingId ? '编辑笔记' : '新建笔记'" width="540px">
      <el-form label-width="56px">
        <el-form-item label="标题">
          <el-input
            v-model="form.title"
            maxlength="200"
            show-word-limit
            placeholder="给它起个名字"
          />
        </el-form-item>
        <el-form-item label="内容">
          <el-input
            v-model="form.content"
            type="textarea"
            :rows="6"
            placeholder="想到什么就写什么…"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.time {
  color: var(--ink-500);
  font-size: 13px;
}

.pager {
  justify-content: flex-end;
  margin-top: 18px;
}
</style>
