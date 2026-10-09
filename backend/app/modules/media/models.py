"""媒体模块的 SQLAlchemy 模型。

文件本体存在磁盘（upload_dir），这里只存元信息；不建到笔记的外键 ——
媒体是共享能力，笔记正文里只引用它的 URL。
"""

import uuid
from datetime import datetime

from sqlalchemy import BigInteger, DateTime, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, SoftDeleteMixin


class Media(SoftDeleteMixin, Base):
    __tablename__ = "media"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=func.uuidv7())
    kind: Mapped[str] = mapped_column(String(16), index=True)  # image | audio | video
    path: Mapped[str] = mapped_column(String(300))  # 相对 upload_dir 的正斜杠路径
    original_name: Mapped[str] = mapped_column(String(255))  # 仅用于展示，绝不参与磁盘路径
    mime: Mapped[str] = mapped_column(String(100))
    size: Mapped[int] = mapped_column(BigInteger())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
