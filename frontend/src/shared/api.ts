import axios from 'axios'
import { ElMessage } from 'element-plus'

/**
 * 统一的 API 客户端。
 * - baseURL 指向 /api/v1，开发时由 Vite 代理转发到后端（见 vite.config.ts）
 * - 错误统一提示；业务代码只管拿数据
 */
export const api = axios.create({
  baseURL: '/api/v1',
  timeout: 15000,
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    const detail = error?.response?.data?.detail
    ElMessage.error(typeof detail === 'string' ? detail : '请求失败，请稍后重试')
    return Promise.reject(error)
  },
)
