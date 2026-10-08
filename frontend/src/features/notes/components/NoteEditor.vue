<script setup lang="ts">
import { computed, ref, useId } from 'vue'
import { MdEditor, NormalToolbar } from 'md-editor-v3'
import type { ExposeParam, Footers, ToolbarNames } from 'md-editor-v3'
import { Headset, Picture, VideoPlay } from '@element-plus/icons-vue'

import { useMediaUpload } from '../composables/useMediaUpload'
import MediaPickButtons from './MediaPickButtons.vue'

const props = withDefaults(
  defineProps<{
    modelValue: string
    mode?: 'article' | 'quick'
    placeholder?: string
    height?: string
    disabled?: boolean
  }>(),
  { mode: 'article', placeholder: '写点什么…', disabled: false },
)

const emit = defineEmits<{
  'update:modelValue': [string]
  save: []
}>()

// md-editor 的事件总线是模块级单例、以 id 为 key —— 每个实例必须是唯一 id，
// 否则同一事件会触发多次（内容插两遍）。
const editorId = `note-editor-${useId()}`
const editorRef = ref<ExposeParam>()

const boxHeight = computed(
  () => props.height ?? (props.mode === 'quick' ? '180px' : 'calc(100vh - 300px)'),
)

const { pick, uploadFiles } = useMediaUpload((markdown) => {
  editorRef.value?.insert(() => ({ targetValue: markdown, select: false }))
})

// 文章模式的工具栏白名单。刻意不含：
// preview/previewOnly/catalog（预览已关、无需目录）、prettier（未装包会报错）、
// mermaid/katex/github（这些是运行时从 CDN 拉的，国内可能卡住）
const ARTICLE_TOOLBARS: ToolbarNames[] = [
  'bold',
  'italic',
  'strikeThrough',
  '-',
  'title',
  'quote',
  'unorderedList',
  'orderedList',
  'task',
  '-',
  'codeRow',
  'code',
  'link',
  'table',
  '-',
  0,
  1,
  2,
  '-',
  'revoke',
  'next',
  '=',
  'pageFullscreen',
]

const toolbars = computed<ToolbarNames[]>(() => (props.mode === 'quick' ? [] : ARTICLE_TOOLBARS))
const footers = computed<Footers[]>(() => (props.mode === 'quick' ? [] : ['markdownTotal']))

function onPasteCapture(e: ClipboardEvent) {
  const files = Array.from(e.clipboardData?.files ?? [])
  if (!files.length) return // 纯文本 → 交给编辑器
  if (files.every((f) => f.type.startsWith('image/'))) return // 纯图片 → 交给内置 onUploadImg
  // 含非图片：内置粘贴处理器只认图片、会把其余的吞掉，这里整批接管
  e.preventDefault()
  e.stopPropagation()
  void uploadFiles(files)
}

function onDropCapture(e: DragEvent) {
  const files = Array.from(e.dataTransfer?.files ?? [])
  if (!files.length) return // 不是文件（例如拖动选中的文字）→ 不干预
  e.preventDefault()
  e.stopPropagation()
  void uploadFiles(files)
}

/** 内置图片入口（图片下拉、粘贴图片）也走同一条链路 */
function onUploadImg(files: File[], callback: (urls: string[]) => void) {
  if (files?.length) void uploadFiles(files)
  callback([]) // 内容由我们自己的 insert 负责，回空数组避免插入两次
}
</script>

<template>
  <div @paste.capture="onPasteCapture" @dragover.prevent @drop.capture="onDropCapture">
    <MdEditor
      :id="editorId"
      ref="editorRef"
      :model-value="modelValue"
      :preview="false"
      theme="light"
      language="zh-CN"
      :placeholder="placeholder"
      :disabled="disabled"
      :toolbars="toolbars"
      :footers="footers"
      :no-mermaid="true"
      :no-katex="true"
      :no-echarts="true"
      :no-highlight="true"
      :style="{ height: boxHeight }"
      @update:model-value="emit('update:modelValue', $event)"
      @on-save="emit('save')"
      @on-upload-img="onUploadImg"
    >
      <template #defToolbars>
        <NormalToolbar title="插入图片" @on-click="pick('image')">
          <el-icon><Picture /></el-icon>
        </NormalToolbar>
        <NormalToolbar title="插入音频" @on-click="pick('audio')">
          <el-icon><Headset /></el-icon>
        </NormalToolbar>
        <NormalToolbar title="插入视频" @on-click="pick('video')">
          <el-icon><VideoPlay /></el-icon>
        </NormalToolbar>
      </template>
    </MdEditor>

    <!-- 小记模式没有工具栏，媒体入口放外面一行 -->
    <MediaPickButtons v-if="mode === 'quick'" @pick="pick" />
  </div>
</template>
