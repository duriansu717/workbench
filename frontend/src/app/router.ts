import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

import AppLayout from '@/app/AppLayout.vue'
import HomeView from '@/app/HomeView.vue'

/**
 * 路由装配。
 * 每个功能在自己的 features/<名>/routes.ts 里声明路由（相对路径，挂在布局之下），
 * 这里自动收集 —— 新增功能不用改这个文件。
 */
const featureModules = import.meta.glob<{ default: RouteRecordRaw[] }>('../features/*/routes.ts', {
  eager: true,
})

const featureRoutes = Object.values(featureModules).flatMap((mod) => mod.default)

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: AppLayout,
      children: [{ path: '', name: 'home', component: HomeView }, ...featureRoutes],
    },
  ],
})

export default router
