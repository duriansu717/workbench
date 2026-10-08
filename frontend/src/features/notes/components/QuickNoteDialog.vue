<script setup lang="ts">
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'

import { createNote, updateNote } from '../api'
import NoteEditor from './NoteEditor.vue'
import type { Note } from '@/shared/types'

const props = defineProps<{ modelValue: boolean; note?: Note | null }>()
const emit = defineEmits<{ 'update:modelValue': [boolean]; saved: [] }>()

const content = ref('')
const saving = ref(false)

watch(
  () => props.modelValue,
  (open) => {
    if (open) content.value = props.note?.content ?? ''
  },
)

async function save() {
  if (!content.value.trim()) {
    ElMessage.warning('内容不能为空')
    return
  }
  saving.value = true
  try {
    if (props.note) {
      await updateNote(props.note.id, { content: content.value })
      ElMessage.success('已保存')
    } else {
      await createNote({ kind: 'quick', content: content.value })
      ElMessage.success('已记下')
    }
    emit('update:modelValue', false)
    emit('saved')
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <el-dialog
    :model-value="modelValue"
    :title="note ? '编辑小记' : '写一条'"
    width="620px"
    @update:model-value="emit('update:modelValue', $event)"
  >
    <NoteEditor
      v-model="content"
      mode="quick"
      height="220px"
      placeholder="随手记点什么…"
      @save="save"
    />
    <template #footer>
      <el-button @click="emit('update:modelValue', false)">取消</el-button>
      <el-button type="primary" :loading="saving" @click="save">保存</el-button>
    </template>
  </el-dialog>
</template>
