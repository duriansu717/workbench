"""媒体上传的校验与落盘。

安全要点：磁盘文件名**从不使用用户提供的文件名**，只用 uuid4 + 白名单扩展名，
所以 `..`、`C:\\`、Windows 保留名（CON/NUL）、中文名等一律天然免疫。
"""

import mimetypes
import shutil
import uuid as uuid_lib
from datetime import UTC, datetime
from pathlib import Path
from typing import BinaryIO

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.concurrency import run_in_threadpool

from app.core.config import settings
from app.modules.media.constants import EXT_KIND, EXT_MIME
from app.modules.media.models import Media


def _safe_name(filename: str | None) -> str:
    """只保留文件名本身，剥掉任何路径分隔符（顺带挡住 ../.. 这类穿越）。"""
    return (filename or "").replace("\\", "/").rsplit("/", 1)[-1]


def _too_large_detail() -> str:
    return f"文件超过 {settings.upload_max_size // (1024 * 1024)}MB 上限"


def _copy(src: BinaryIO, dest: Path) -> int:
    """同步复制（放线程池里跑，避免阻塞事件循环）。"""
    with dest.open("wb") as out:
        shutil.copyfileobj(src, out, 1024 * 1024)
    return dest.stat().st_size


async def save_upload(db: AsyncSession, upload: UploadFile) -> Media:
    name = _safe_name(upload.filename)
    ext = Path(name).suffix.lower().lstrip(".")
    if not ext:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="文件名缺少扩展名")
    if ext not in settings.upload_allowed_ext:
        allowed = "、".join(f".{e}" for e in settings.upload_allowed_ext)
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"不支持的文件类型 .{ext}；允许：{allowed}",
        )
    if upload.size and upload.size > settings.upload_max_size:
        raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=_too_large_detail())

    now = datetime.now(UTC)
    rel = f"{now:%Y}/{now:%m}/{uuid_lib.uuid4().hex}.{ext}"
    dest = settings.upload_dir / rel
    dest.parent.mkdir(parents=True, exist_ok=True)

    # 兜底：确认落点没有被带出 upload_dir
    if not dest.resolve().is_relative_to(settings.upload_dir.resolve()):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="非法的文件路径")

    await upload.seek(0)
    size = await run_in_threadpool(_copy, upload.file, dest)

    def cleanup() -> None:
        dest.unlink(missing_ok=True)

    # 落盘后再核对一次真实字节数（upload.size 可能缺失或被伪造）
    if size > settings.upload_max_size:
        cleanup()
        raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail=_too_large_detail())
    if size == 0:
        cleanup()
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="文件内容为空")

    media = Media(
        kind=EXT_KIND[ext],
        path=rel,
        original_name=name[:255],
        mime=EXT_MIME.get(ext) or mimetypes.guess_type(name)[0] or "application/octet-stream",
        size=size,
    )
    db.add(media)
    try:
        await db.commit()
    except Exception:
        cleanup()  # 入库失败就别把文件留在磁盘上
        raise
    await db.refresh(media)
    return media
