/**
 * Markdown 渲染（模块级单例）。
 *
 * 关键设计：正文里媒体就是普通 Markdown —— `![名称](/media/2026/10/xxx.mp4)`，
 * 由 **文件扩展名** 决定渲染成 <img> / <audio> / <video>，
 * 这样列表、详情、预览三处表现完全一致。
 */
import DOMPurify from 'dompurify'
import MarkdownIt from 'markdown-it'

const AUDIO_EXT = new Set(['mp3', 'wav', 'ogg', 'm4a', 'flac'])
const VIDEO_EXT = new Set(['mp4', 'webm', 'mov'])

const md = new MarkdownIt({
  html: false, // 正文里的原始 HTML 一律转义（只有下面自己产出的标签才会输出）
  linkify: true,
  breaks: true, // 单个换行即换行 —— 符合"随手记"的直觉
})

const defaultImage = md.renderer.rules.image!
const esc = md.utils.escapeHtml

md.renderer.rules.image = (tokens, idx, options, env, self) => {
  const token = tokens[idx]
  if (!token) return ''
  const rawSrc = token.attrGet('src')
  const src = rawSrc == null ? '' : String(rawSrc)
  const clean = src.split(/[?#]/)[0] ?? ''
  const ext = clean.split('.').pop()?.toLowerCase() ?? ''
  const alt = esc(String(token.content || ''))

  if (AUDIO_EXT.has(ext)) {
    return `<audio controls preload="metadata" src="${esc(src)}" title="${alt}"></audio>`
  }
  if (VIDEO_EXT.has(ext)) {
    return `<video controls preload="metadata" playsinline src="${esc(src)}" title="${alt}"></video>`
  }
  return defaultImage(tokens, idx, options, env, self)
}

export function renderMarkdown(source?: string | null): string {
  return DOMPurify.sanitize(md.render(source ?? ''), {
    ADD_TAGS: ['audio', 'video', 'source'],
    ADD_ATTR: ['controls', 'preload', 'playsinline', 'poster', 'title'],
  })
}

/** 从 Markdown 正文里挤出一小段纯文本，列表页做摘要用 */
export function plainText(source?: string | null, limit = 90): string {
  const text = (source ?? '')
    .replace(/```[\s\S]*?```/g, ' ') // 代码块整段丢掉
    .replace(/!\[[^\]]*\]\([^)]*\)/g, '［媒体］') // 图片/音视频 → 占位
    .replace(/\[([^\]]*)\]\([^)]*\)/g, '$1') // 链接只留文字
    .replace(/^\s{0,3}#{1,6}\s+/gm, '') // 标题符号
    .replace(/^\s{0,3}>\s?/gm, '') // 引用符号
    .replace(/^\s{0,3}[-*+]\s+/gm, '') // 列表符号
    .replace(/[*_`~|]/g, '')
    .replace(/\s+/g, ' ')
    .trim()
  return text.length > limit ? `${text.slice(0, limit)}…` : text
}
