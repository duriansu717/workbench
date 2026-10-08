import type { RouteRecordRaw } from 'vue-router'

// 本功能的路由（相对布局的子路径）；app/router.ts 会自动收集。
// 注意：静态段写在动态段前面，纯粹是为了好读（vue-router 自己会按具体度打分）。
export default [
  {
    path: 'notes',
    name: 'notes',
    component: () => import('./NotesView.vue'),
  },
  {
    path: 'notes/articles/new',
    name: 'note-article-new',
    component: () => import('./ArticleEditView.vue'),
  },
  {
    path: 'notes/articles/:id',
    name: 'note-article',
    component: () => import('./ArticleDetailView.vue'),
  },
  {
    path: 'notes/articles/:id/edit',
    name: 'note-article-edit',
    component: () => import('./ArticleEditView.vue'),
  },
] satisfies RouteRecordRaw[]
