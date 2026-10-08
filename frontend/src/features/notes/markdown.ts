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
