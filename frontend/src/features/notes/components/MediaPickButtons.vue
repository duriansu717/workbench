<script setup lang="ts">
import { Headset, Picture, VideoPlay } from '@element-plus/icons-vue'

import type { MediaKind } from '@/shared/types'

const emit = defineEmits<{ pick: [MediaKind] }>()
</script>

<template>
  <div class="media-picks">
    <el-button link :icon="Picture" @click="emit('pick', 'image')">图片</el-button>
    <el-button link :icon="Headset" @click="emit('pick', 'audio')">音频</el-button>
    <el-button link :icon="VideoPlay" @click="emit('pick', 'video')">视频</el-button>
    <span class="hint">也可直接粘贴或拖入文件</span>
  </div>
</template>

<style scoped>
.media-picks {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 8px;
}

.hint {
  margin-left: 8px;
  color: var(--ink-400);
  font-size: 12px;
}
</style>
