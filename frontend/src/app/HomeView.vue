<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Right } from '@element-plus/icons-vue'

import { api } from '@/shared/api'
import { resolveFeatureIcon } from '@/shared/featureIcons'
import type { ModuleMeta } from '@/shared/types'

const router = useRouter()
const features = ref<ModuleMeta[]>([])

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 5) return '夜深了'
  if (h < 9) return '早上好'
  if (h < 12) return '上午好'
  if (h < 14) return '中午好'
  if (h < 18) return '下午好'
  return '晚上好'
})

const today = computed(() =>
  new Date().toLocaleDateString('zh-CN', { month: 'long', day: 'numeric', weekday: 'long' }),
)

onMounted(async () => {
  // 首页宫格 = 后端功能注册表，加功能自动出现（hidden 的共享模块不显示）
  const { data } = await api.get<ModuleMeta[]>('/modules')
  features.value = data.filter((m) => !m.hidden)
})
</script>

<template>
  <div class="home">
    <header class="hero">
      <h1 class="hello">{{ greeting }}，欢迎回来 ☀️</h1>
      <p class="sub">{{ today }} · 今天想从哪件小事开始？</p>
    </header>

    <section>
      <div class="section-head">
        <h2 class="section-title">我的功能</h2>
        <span class="section-hint">一共 {{ features.length }} 个</span>
      </div>

      <div class="grid">
        <button
          v-for="item in features"
          :key="item.name"
          type="button"
          class="card"
          @click="router.push(item.path)"
        >
          <span class="tile">
            <el-icon :size="20"><component :is="resolveFeatureIcon(item.icon)" /></el-icon>
          </span>
          <span class="title">{{ item.title }}</span>
          <span class="desc">{{ item.description }}</span>
          <el-icon class="arrow"><Right /></el-icon>
        </button>

        <div v-if="!features.length" class="empty">
          还没有功能模块，在 backend/app/modules/ 里加一个就会出现
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.hero {
  position: relative;
  padding: 4px 0 30px;
}

.hello {
  margin: 0;
  font-size: 27px;
  letter-spacing: 0.5px;
}

.sub {
  margin: 10px 0 0;
  color: var(--ink-500);
  font-size: 14px;
}

.section-head {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-bottom: 14px;
}

.section-title {
  margin: 0;
  font-size: 16px;
  color: var(--ink-900);
}

.section-hint {
  font-size: 12px;
  color: var(--ink-400);
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(230px, 1fr));
  gap: 16px;
}

/* 功能卡片：暖白渐变 + 悬停轻抬 */
.card {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 20px;
  text-align: left;
  font: inherit;
  color: inherit;
  cursor: pointer;
  border: 1px solid var(--warm-line-soft);
  border-radius: var(--warm-radius-lg);
  background: linear-gradient(160deg, #fffdf9 0%, #fff6e8 100%);
  box-shadow: var(--warm-shadow-sm);
  transition:
    transform 0.18s ease,
    box-shadow 0.18s ease,
    border-color 0.18s ease;
}

.card:hover {
  transform: translateY(-4px);
  border-color: #f2d9ae;
  box-shadow: var(--warm-shadow-md);
}

.card:focus-visible {
  outline: 2px solid var(--honey-500);
  outline-offset: 2px;
}

.tile {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  margin-bottom: 4px;
  border-radius: 13px;
  color: var(--honey-800);
  background: linear-gradient(140deg, var(--honey-100), #ffe9c2);
  box-shadow: inset 0 0 0 1px rgba(232, 163, 61, 0.18);
}

.title {
  font-size: 15px;
  font-weight: 600;
  color: var(--ink-900);
}

.desc {
  font-size: 12.5px;
  line-height: 1.5;
  color: var(--ink-500);
}

.arrow {
  position: absolute;
  right: 16px;
  bottom: 18px;
  color: var(--honey-300);
  opacity: 0;
  transform: translateX(-4px);
  transition:
    opacity 0.18s ease,
    transform 0.18s ease;
}

.card:hover .arrow {
  opacity: 1;
  transform: translateX(0);
}

.empty {
  padding: 28px;
  border: 1px dashed var(--warm-line);
  border-radius: var(--warm-radius);
  color: var(--ink-400);
  font-size: 13px;
  text-align: center;
}
</style>
