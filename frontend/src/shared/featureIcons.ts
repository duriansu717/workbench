import type { Component } from 'vue'
import {
  Calendar,
  ChatDotRound,
  Coffee,
  CoffeeCup,
  Coin,
  Collection,
  DataLine,
  Document,
  Film,
  Folder,
  Grid,
  Headset,
  Link,
  MagicStick,
  Memo,
  Mic,
  Moon,
  Notebook,
  Picture,
  Setting,
  Star,
  Sunny,
  Sunrise,
  Sunset,
  Timer,
  VideoPlay,
} from '@element-plus/icons-vue'

/**
 * 功能注册表（后端 registry.py 的 icon 字段）→ 图标组件。
 * 需要新图标时在这里登记一个即可；没登记的名字会退回默认图标。
 * 图标名必须是 @element-plus/icons-vue 真实导出的名字。
 */
const icons: Record<string, Component> = {
  Calendar,
  ChatDotRound,
  Coffee,
  CoffeeCup,
  Coin,
  Collection,
  DataLine,
  Document,
  Film,
  Folder,
  Headset,
  Link,
  MagicStick,
  Memo,
  Mic,
  Moon,
  Notebook,
  Picture,
  Setting,
  Star,
  Sunny,
  Sunrise,
  Sunset,
  Timer,
  VideoPlay,
}

export function resolveFeatureIcon(name?: string): Component {
  return (name && icons[name]) || Grid
}
