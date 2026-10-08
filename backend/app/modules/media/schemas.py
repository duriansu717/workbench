"""媒体模块的 Pydantic 出入参。"""

import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, computed_field

MediaKind = Literal["image", "audio", "video"]


class MediaRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    kind: MediaKind
    path: str
    original_name: str
    mime: str
    size: int
    created_at: datetime

    @computed_field  # type: ignore[prop-decorator]
    @property
    def url(self) -> str:
        """对外访问路径（前端直接拼进 Markdown）。"""
        return f"/media/{self.path}"


class MediaConfig(BaseModel):
    """前端用它设置 accept、以及上传前预检（避免传完才发现超限）。"""

    max_size: int
    allowed_ext: list[str]
    image_ext: list[str]
    audio_ext: list[str]
    video_ext: list[str]
    upload_endpoint: str = "/api/v1/media"
