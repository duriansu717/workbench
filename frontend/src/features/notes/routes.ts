import type { RouteRecordRaw } from 'vue-router'

// 本功能的路由（相对布局的子路径）；app/router.ts 会自动收集
export default [
  {
    path: 'notes',
    name: 'notes',
    component: () => import('./NotesView.vue'),
  },
] satisfies RouteRecordRaw[]
