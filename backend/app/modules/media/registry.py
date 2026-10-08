"""媒体模块的元信息。

hidden=True：它是各功能共用的能力（有 /api/v1/media 路由和 /media 静态目录），
但**不出现在侧边栏与首页宫格**。
"""

META: dict = {
    "title": "媒体",
    "description": "图片 / 音频 / 视频上传",
    "icon": "Picture",
    "path": "/media",
    "hidden": True,
}
