"""媒体模块的路由。

注意：/config 必须声明在 /{media_id} **之前**，否则 "config" 会被当成 UUID
去解析并返回 422。
"""

import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_db
from app.modules.media import service
from app.modules.media.constants import EXT_KIND
from app.modules.media.models import Media
from app.modules.media.schemas import MediaConfig, MediaRead

router = APIRouter()

NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="媒体不存在")


@router.get("/config", response_model=MediaConfig, summary="上传配置（允许类型与大小上限）")
async def get_config() -> MediaConfig:
    by_kind: dict[str, list[str]] = {"image": [], "audio": [], "video": []}
    for ext in settings.upload_allowed_ext:
        by_kind[EXT_KIND[ext]].append(ext)
    return MediaConfig(
        max_size=settings.upload_max_size,
        allowed_ext=settings.upload_allowed_ext,
        image_ext=by_kind["image"],
        audio_ext=by_kind["audio"],
        video_ext=by_kind["video"],
    )


@router.post(
    "",
    response_model=MediaRead,
    status_code=status.HTTP_201_CREATED,
    summary="上传媒体文件（multipart，字段名 file）",
)
async def upload_media(
    file: UploadFile = File(...), db: AsyncSession = Depends(get_db)
) -> MediaRead:
    media = await service.save_upload(db, file)
    return MediaRead.model_validate(media)


@router.get("/{media_id}", response_model=MediaRead, summary="媒体元信息")
async def get_media(media_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> MediaRead:
    media = await db.get(Media, media_id)
    if media is None:
        raise NOT_FOUND
    return MediaRead.model_validate(media)
