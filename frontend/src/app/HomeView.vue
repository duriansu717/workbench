<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import { api } from '@/shared/api'
import type { ModuleMeta } from '@/shared/types'

const router = useRouter()
const features = ref<ModuleMeta[]>([])

onMounted(async () => {
  // 首页宫格 = 后端功能注册表，加功能自动出现
  features.value = (await api.get<ModuleMeta[]>('/modules')).data
})
</script>

<template>
  <div>
    <h2>功能</h2>
    <div class="grid">
      <el-card
        v-for="item in features"
        :key="item.name"
        class="card"
        shadow="hover"
        @click="router.push(item.path)"
      >
        <div class="title">{{ item.title }}</div>
        <div class="desc">{{ item.description }}</div>
      </el-card>
    </div>
  </div>
</template>

<style scoped>
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.card {
  cursor: pointer;
}

.title {
  font-size: 16px;
  font-weight: 600;
}

.desc {
  margin-top: 8px;
  color: var(--el-text-color-secondary);
  font-size: 13px;
}
</style>
