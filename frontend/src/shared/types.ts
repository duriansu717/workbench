/**
 * 前端类型统一从后端 OpenAPI 自动生成，不要手写。
 * 生成命令：pnpm gen:api-types（需要后端在 8000 端口运行）
 */
import type { components } from './api-types'

/** 功能元信息（GET /api/v1/modules） */
export type ModuleMeta = components['schemas']['ModuleMeta']

/** 笔记：quick = 随手小记（title 恒为 null），article = 文章 */
export type Note = components['schemas']['NoteRead']
export type NoteCreate = components['schemas']['NoteCreate']
export type NoteUpdate = components['schemas']['NoteUpdate']
export type NoteKind = Note['kind']

/** 媒体（图片 / 音频 / 视频） */
export type Media = components['schemas']['MediaRead']
export type MediaConfig = components['schemas']['MediaConfig']
export type MediaKind = Media['kind']

/** 后端统一分页返回（对应 app/core/schemas.py 的 Page[T]） */
export interface Page<T> {
  items: T[]
  total: number
}
