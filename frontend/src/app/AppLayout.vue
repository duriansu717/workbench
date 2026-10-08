<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { House } from '@element-plus/icons-vue'

import { api } from '@/shared/api'
import { resolveFeatureIcon } from '@/shared/featureIcons'
import type { ModuleMeta } from '@/shared/types'

const route = useRoute()
const features = ref<ModuleMeta[]>([])

onMounted(async () => {
  // 菜单由后端的功能注册表驱动：加了新模块，这里自动出现
  features.value = (await api.get<ModuleMeta[]>('/modules')).data
})
</script>

<template>
  <div class="layout">
    <aside class="sidebar">
      <div class="brand">
        <span class="sun" />
        <div>
          <div class="brand-name">工作台</div>
          <div class="brand-sub">我的小天地</div>
        </div>
      </div>

      <el-menu router :default-active="route.path" class="nav">
        <el-menu-item index="/">
          <el-icon><House /></el-icon>
          <span>首页</span>
        </el-menu-item>
        <el-menu-item v-for="item in features" :key="item.name" :index="item.path">
          <el-icon><component :is="resolveFeatureIcon(item.icon)" /></el-icon>
          <span>{{ item.title }}</span>
        </el-menu-item>
      </el-menu>

      <div class="sidebar-foot">今天也慢慢来 ☕</div>
    </aside>

    <main class="main">
      <div class="container">
        <RouterView />
      </div>
    </main>
  </div>
</template>

<style scoped>
.layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

/* ---- 侧边栏 ---- */
.sidebar {
  display: flex;
  flex-direction: column;
  width: 232px;
  flex-shrink: 0;
  background: linear-gradient(180deg, #fff8ea 0%, #fbefda 100%);
  border-right: 1px solid var(--warm-line-soft);
}

.brand {
  position: relative;
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 22px 20px 18px;
}

/* 品牌区后面一团暖光，像清晨的太阳 */
.brand::before {
  content: '';
  position: absolute;
  left: -40px;
  top: -70px;
  width: 190px;
  height: 190px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 196, 92, 0.42) 0%, rgba(255, 196, 92, 0) 70%);
  pointer-events: none;
}

.sun {
  position: relative;
  width: 30px;
  height: 30px;
  flex-shrink: 0;
  border-radius: 50%;
  background: linear-gradient(140deg, #ffd98a, var(--honey-500));
  box-shadow: 0 0 0 6px rgba(232, 163, 61, 0.16);
}

.brand-name {
  font-size: 17px;
  font-weight: 700;
  color: var(--ink-900);
  letter-spacing: 0.5px;
}

.brand-sub {
  margin-top: 2px;
  font-size: 12px;
  color: var(--ink-400);
}

.nav {
  flex: 1;
  padding-top: 6px;
  overflow-y: auto;
}

.sidebar-foot {
  padding: 16px 20px 18px;
  font-size: 12px;
  color: var(--ink-400);
}

/* ---- 内容区 ---- */
.main {
  flex: 1;
  overflow-y: auto;
}

.container {
  max-width: 1180px;
  margin: 0 auto;
  padding: 30px 34px 48px;
}
</style>
