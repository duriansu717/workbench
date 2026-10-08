"""媒体类型与 MIME 映射。

上传校验、静态服务、前端渲染三处共用同一张表，避免各写一份对不上。
"""

import mimetypes

# 扩展名 → MIME
EXT_MIME: dict[str, str] = {
    # 图片
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "webp": "image/webp",
    "avif": "image/avif",
    # 音频
    "mp3": "audio/mpeg",
    "wav": "audio/wav",
    "ogg": "audio/ogg",
    "m4a": "audio/mp4",
    "flac": "audio/flac",
    # 视频
    "mp4": "video/mp4",
    "webm": "video/webm",
    "mov": "video/quicktime",
}

# 扩展名 → 大类；前端按这个决定渲染 <img> / <audio> / <video>
EXT_KIND: dict[str, str] = {
    **dict.fromkeys(("jpg", "jpeg", "png", "gif", "webp", "avif"), "image"),
    **dict.fromkeys(("mp3", "wav", "ogg", "m4a", "flac"), "audio"),
    **dict.fromkeys(("mp4", "webm", "mov"), "video"),
}


def register_mimetypes() -> None:
    """启动时把扩展名显式注册进 mimetypes。

    Windows 上 mimetypes 会去读注册表，.webm / .m4a / .flac / .avif 可能拿不到
    正确的 MIME，StaticFiles 就会回 application/octet-stream，导致 <video> 不播放。
    """
    for ext, mime in EXT_MIME.items():
        mimetypes.add_type(mime, f".{ext}")
