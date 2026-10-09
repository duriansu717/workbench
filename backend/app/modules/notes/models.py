"""笔记模块的 SQLAlchemy 模型。

两种模式共用一张表，用 kind 区分：
- quick   随手小记：没有标题，正文短
- article 文章：有标题，正文是完整的 Markdown

继承 SoftDeleteMixin：删除是逻辑删除（只打 deleted_at 标记），查询默认自动过滤掉。
"""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base, SoftDeleteMixin


class Note(SoftDeleteMixin, Base):
    __tablename__ = "notes"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, server_default=func.uuidv7())
    kind: Mapped[str] = mapped_column(String(16), server_default="quick", index=True)
    title: Mapped[str | None] = mapped_column(String(200))  # 仅文章有标题
    content: Mapped[str | None] = mapped_column(Text)  # Markdown 正文
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
