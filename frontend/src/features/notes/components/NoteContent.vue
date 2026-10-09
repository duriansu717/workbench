<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

import { renderMarkdown } from '../markdown'

const props = withDefaults(defineProps<{ content?: string | null; compact?: boolean }>(), {
  content: '',
  compact: false,
})

const html = computed(() => renderMarkdown(props.content))
const root = ref<HTMLDivElement>()

/**
 * 视频放不出来时给一句人话提示，而不是留一块黑屏。
 * 典型原因：H.265/HEVC 编码（Chrome/Edge 在 Windows 上解不了）。
 * 用事件委托挂在容器上 —— 非冒泡事件靠捕获阶段也能收到，v-html 重渲染也不受影响。
 */
function onMediaEvent(e: Event) {
  const el = e.target
  if (!(el instanceof HTMLVideoElement)) return
  const broken = e.type === 'error' || (e.type === 'loadedmetadata' && el.videoWidth === 0)
  if (!broken || el.dataset.tip) return
  el.dataset.tip = '1'
  el.classList.add('is-broken')

  const tip = document.createElement('p')
  tip.className = 'media-tip'
  tip.textContent = '这个视频浏览器解不了（多半是 H.265/HEVC 编码）。转成 H.264 的 mp4 就能播。'
  el.insertAdjacentElement('afterend', tip)
}

/** 点图片在新标签看原图（没被链接包住的图片才处理） */
function onClick(e: MouseEvent) {
  const el = e.target
  if (!(el instanceof HTMLImageElement) || el.closest('a')) return
  window.open(el.currentSrc || el.src, '_blank', 'noopener')
}

onMounted(() => {
  root.value?.addEventListener('error', onMediaEvent, true)
  root.value?.addEventListener('loadedmetadata', onMediaEvent, true)
  root.value?.addEventListener('click', onClick)
})

onBeforeUnmount(() => {
  root.value?.removeEventListener('error', onMediaEvent, true)
  root.value?.removeEventListener('loadedmetadata', onMediaEvent, true)
  root.value?.removeEventListener('click', onClick)
})
</script>

<template>
  <!-- 内容来自我们自己的 markdown-it 渲染 + DOMPurify 过滤，不是用户原始 HTML -->
  <div ref="root" class="note-content" :class="{ compact }" v-html="html" />
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

/* ---- 媒体：都限高限宽并居中，竖版照片不会铺满整列 ---- */
.note-content :deep(img) {
  display: block;
  width: auto;
  height: auto;
  max-width: 100%;
  max-height: 560px;
  margin: 12px auto;
  border-radius: var(--warm-radius);
  cursor: zoom-in;
}

.note-content :deep(video) {
  display: block;
  max-width: min(100%, 720px);
  max-height: 560px;
  margin: 12px auto;
  border-radius: var(--warm-radius);
  background: #000;
}

/* 解不出来的视频别占一大块，缩成一条并显示提示 */
.note-content :deep(video.is-broken) {
  max-height: 170px;
  opacity: 0.55;
}

.note-content :deep(.media-tip) {
  margin: 6px 0 14px;
  padding: 8px 12px;
  border-radius: 10px;
  background: var(--honey-50);
  color: var(--ink-500);
  font-size: 12.5px;
}

.note-content :deep(audio) {
  display: block;
  max-width: 520px;
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
  max-height: 300px;
  margin: 8px 0;
}
</style>
