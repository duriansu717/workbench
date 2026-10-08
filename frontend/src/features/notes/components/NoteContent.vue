<script setup lang="ts">
import { computed } from 'vue'

import { renderMarkdown } from '../markdown'

const props = withDefaults(defineProps<{ content?: string | null; compact?: boolean }>(), {
  content: '',
  compact: false,
})

const html = computed(() => renderMarkdown(props.content))
</script>

<template>
  <!-- 内容来自我们自己的 markdown-it 渲染 + DOMPurify 过滤，不是用户原始 HTML -->
  <div class="note-content" :class="{ compact }" v-html="html" />
</template>

<style scoped>
.note-content {
  color: var(--ink-700);
  font-size: 15px;
  line-height: 1.85;
  word-break: break-word;
}

.note-content :deep(h1),
.note-content :deep(h2),
.note-content :deep(h3) {
  margin: 20px 0 10px;
  color: var(--ink-900);
}
.note-content :deep(h1) {
  font-size: 23px;
}
.note-content :deep(h2) {
  font-size: 19px;
}
.note-content :deep(h3) {
  font-size: 16.5px;
}
.note-content :deep(p) {
  margin: 10px 0;
}
.note-content :deep(a) {
  color: var(--honey-700);
  text-decoration: underline;
  text-underline-offset: 2px;
}
.note-content :deep(blockquote) {
  margin: 12px 0;
  padding: 8px 14px;
  border-left: 3px solid var(--honey-300);
  border-radius: 0 8px 8px 0;
  background: var(--honey-50);
  color: var(--ink-500);
}
.note-content :deep(code) {
  padding: 2px 6px;
  border-radius: 6px;
  background: var(--warm-canvas-soft);
  font-size: 13.5px;
}
.note-content :deep(pre) {
  margin: 12px 0;
  padding: 14px 16px;
  border-radius: var(--warm-radius);
  background: var(--warm-canvas-soft);
  overflow-x: auto;
}
.note-content :deep(pre code) {
  padding: 0;
  background: none;
}
.note-content :deep(img),
.note-content :deep(video) {
  display: block;
  max-width: 100%;
  margin: 12px 0;
  border-radius: var(--warm-radius);
}
.note-content :deep(video) {
  background: #000;
}
.note-content :deep(audio) {
  display: block;
  width: 100%;
  margin: 10px 0;
}
.note-content :deep(table) {
  margin: 12px 0;
  border-collapse: collapse;
}
.note-content :deep(th),
.note-content :deep(td) {
  padding: 6px 10px;
  border: 1px solid var(--warm-line);
}
.note-content :deep(th) {
  background: var(--honey-50);
}
.note-content :deep(hr) {
  margin: 18px 0;
  border: none;
  border-top: 1px solid var(--warm-line-soft);
}
.note-content :deep(ul),
.note-content :deep(ol) {
  margin: 10px 0;
  padding-left: 22px;
}

/* compact：小记时间流里用，整体收紧一档 */
.note-content.compact {
  font-size: 14px;
  line-height: 1.75;
}
.note-content.compact :deep(h1) {
  font-size: 17px;
  margin: 8px 0 6px;
}
.note-content.compact :deep(h2) {
  font-size: 15.5px;
  margin: 8px 0 6px;
}
.note-content.compact :deep(h3) {
  font-size: 14.5px;
  margin: 8px 0 6px;
}
.note-content.compact :deep(p) {
  margin: 6px 0;
}
.note-content.compact :deep(img),
.note-content.compact :deep(video) {
  max-height: 320px;
  margin: 8px 0;
}
</style>
