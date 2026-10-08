import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    // Element Plus：组件按需引入（样式在 main.ts 统一引入全量 CSS，避免动态组件的样式缺失）
    AutoImport({ resolvers: [ElementPlusResolver()], dts: 'src/auto-imports.d.ts' }),
    Components({
      resolvers: [ElementPlusResolver({ importStyle: false })],
      dts: 'src/components.d.ts',
    }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    // 前端固定端口（被占用时直接报错，不悄悄换端口）
    port: 1213,
    strictPort: true,
    proxy: {
      // 开发时把 /api 转发给后端（uvicorn 跑在 127.0.0.1:8000）
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      // 媒体文件（图片/音频/视频）也走代理，否则 dev 下会 404
      '/media': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})
