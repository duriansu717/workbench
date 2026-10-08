/** 笔记功能用到的接口封装（组件里不直接写 URL）。 */
import { api } from '@/shared/api'
import type {
  Media,
  MediaConfig,
  Note,
  NoteCreate,
  NoteKind,
  NoteUpdate,
  Page,
} from '@/shared/types'

export async function listNotes(params: {
  kind?: NoteKind
  page?: number
  size?: number
}): Promise<Page<Note>> {
  const { data } = await api.get<Page<Note>>('/notes', { params })
  return data
}

export async function getNote(id: string): Promise<Note> {
  const { data } = await api.get<Note>(`/notes/${id}`)
  return data
}

export async function createNote(payload: NoteCreate): Promise<Note> {
  const { data } = await api.post<Note>('/notes', payload)
  return data
}

export async function updateNote(id: string, payload: NoteUpdate): Promise<Note> {
  const { data } = await api.patch<Note>(`/notes/${id}`, payload)
  return data
}

export async function removeNote(id: string): Promise<void> {
  await api.delete(`/notes/${id}`)
}

export async function getMediaConfig(): Promise<MediaConfig> {
  const { data } = await api.get<MediaConfig>('/media/config')
  return data
}

/** 上传单个文件。大文件可能很慢，所以单独关掉全局 15s 超时。 */
export async function uploadMedia(file: File): Promise<Media> {
  const form = new FormData()
  form.append('file', file)
  const { data } = await api.post<Media>('/media', form, { timeout: 0 })
  return data
}
