<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import { api } from '@/shared/api'
import type { ModuleMeta } from '@/shared/types'

const route = useRoute()
const features = ref<ModuleMeta[]>([])

onMounted(async () => {
  // 菜单由后端的功能注册表驱动：加了新模块，这里自动出现
  features.value = (await api.get<ModuleMeta[]>('/modules')).data
})
</script>

<template>
  <el-container class="layout">
    <el-aside width="220px" class="sidebar">
      <div class="brand">工作台</div>
      <el-menu router :default-active="route.path">
        <el-menu-item index="/">首页</el-menu-item>
        <el-menu-item v-for="item in features" :key="item.name" :index="item.path">
          {{ item.title }}
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-main>
        <RouterView />
      </el-main>
    </el-container>
  </el-container>
</template>

<style scoped>
.layout {
  height: 100vh;
}

.sidebar {
  border-right: 1px solid var(--el-border-color-light);
}

.brand {
  display: flex;
  align-items: center;
  height: 56px;
  padding: 0 20px;
  font-size: 18px;
  font-weight: 600;
}
</style>
