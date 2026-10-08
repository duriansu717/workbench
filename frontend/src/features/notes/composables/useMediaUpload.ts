import { ElLoading, ElMessage } from 'element-plus'

import { getMediaConfig, uploadMedia } from '../api'
import type { Media, MediaConfig, MediaKind } from '@/shared/types'

/** 上传结果 → 可插入正文的 Markdown 片段 */
function toSnippet(media: Media): string {
  const alt = media.original_name.replace(/\.[^.]+$/, '').replace(/[[\]()]/g, '') || media.kind
  return `![${alt}](${media.url})`
}

/**
 * 媒体上传 + 插入。三种入口（工具栏按钮 / 粘贴 / 拖拽）共用这一份实现。
 * - 上传前按后端 /media/config 的允许清单和大小上限做预检，避免白传
 * - 插入时必须 select: false，否则刚插入的内容会被选中，用户一敲字就没了
 */
export function useMediaUpload(insert: (markdown: string) => void) {
  let config: MediaConfig | null = null
  let uploading = false // 同时只允许一批上传，否则插入顺序会乱

  async function ensureConfig(): Promise<MediaConfig> {
    config ??= await getMediaConfig()
    return config
  }

  function acceptOf(cfg: MediaConfig, kind: MediaKind): string {
    const exts = kind === 'image' ? cfg.image_ext : kind === 'audio' ? cfg.audio_ext : cfg.video_ext
    return exts.map((e) => `.${e}`).join(',')
  }

  /** 打开系统文件选择框（新建 input，用完即弃，避免复用同一个 input 的状态问题） */
  async function pick(kind: MediaKind): Promise<void> {
    const cfg = await ensureConfig()
    const input = document.createElement('input')
    input.type = 'file'
    input.accept = acceptOf(cfg, kind)
    input.multiple = true
    input.onchange = () => {
      const files = Array.from(input.files ?? [])
      if (files.length) void uploadFiles(files)
    }
    input.click()
  }

  async function uploadFiles(files: File[]): Promise<void> {
    if (uploading || !files.length) return
    const cfg = await ensureConfig()

    const accepted: File[] = []
    for (const file of files) {
      const ext = file.name.split('.').pop()?.toLowerCase() ?? ''
      if (!cfg.allowed_ext.includes(ext)) {
        ElMessage.error(`不支持的文件类型：${file.name}`)
      } else if (file.size > cfg.max_size) {
        ElMessage.error(`${file.name} 超过 ${Math.round(cfg.max_size / 1024 / 1024)}MB 上限`)
      } else {
        accepted.push(file)
      }
    }
    if (!accepted.length) return

    uploading = true
    const tip = ElLoading.service({ lock: true, text: '上传中…' })
    const snippets: string[] = []
    try {
      for (const [i, file] of accepted.entries()) {
        if (accepted.length > 1) tip.setText(`上传中 ${i + 1}/${accepted.length}…`)
        snippets.push(toSnippet(await uploadMedia(file)))
      }
    } catch {
      // 失败提示已由 api.ts 的拦截器统一弹出
    } finally {
      tip.close()
      uploading = false
    }

    if (snippets.length) {
      insert(snippets.join('\n\n'))
      ElMessage.success(snippets.length > 1 ? `已插入 ${snippets.length} 个文件` : '已插入')
    }
  }

  return { pick, uploadFiles }
}
