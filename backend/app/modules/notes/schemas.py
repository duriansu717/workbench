"""笔记模块的 Pydantic 出入参。"""

import uuid
from datetime import datetime
from typing import Literal, Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

NoteKind = Literal["quick", "article"]


class NoteCreate(BaseModel):
    kind: NoteKind = "quick"
    title: str | None = Field(default=None, max_length=200)
    content: str | None = None

    @model_validator(mode="after")
    def _check_kind(self) -> Self:
        if self.kind == "article":
            if not (self.title or "").strip():
                raise ValueError("文章必须有标题")
        else:
            # 小记不带标题：由后端兜底，不依赖前端"记得别传"
            self.title = None
        return self


class NoteUpdate(BaseModel):
    """只改内容，不改类型（kind 不可变）。"""

    title: str | None = Field(default=None, max_length=200)
    content: str | None = None


class NoteRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    kind: NoteKind
    title: str | None
    content: str | None
    created_at: datetime
    updated_at: datetime
