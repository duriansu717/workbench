"""笔记模块的业务逻辑。"""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.notes.models import Note
from app.modules.notes.schemas import NoteCreate, NoteKind, NoteUpdate


async def list_notes(
    db: AsyncSession, kind: NoteKind | None = None, page: int = 1, size: int = 20
) -> tuple[list[Note], int]:
    count_stmt = select(func.count()).select_from(Note)
    list_stmt = select(Note)
    if kind:
        count_stmt = count_stmt.where(Note.kind == kind)
        list_stmt = list_stmt.where(Note.kind == kind)

    total = await db.scalar(count_stmt) or 0
    rows = await db.scalars(
        list_stmt.order_by(Note.created_at.desc()).offset((page - 1) * size).limit(size)
    )
    return list(rows), total


async def get_note(db: AsyncSession, note_id: uuid.UUID) -> Note | None:
    return await db.get(Note, note_id)


async def create_note(db: AsyncSession, data: NoteCreate) -> Note:
    note = Note(**data.model_dump())
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return note


async def update_note(db: AsyncSession, note: Note, data: NoteUpdate) -> Note:
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(note, field, value)
    if note.kind == "quick":
        note.title = None  # 小记永远没有标题（即便客户端传了）
    await db.commit()
    await db.refresh(note)
    return note


async def delete_note(db: AsyncSession, note: Note) -> None:
    await db.delete(note)
    await db.commit()
