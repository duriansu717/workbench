"""笔记模块的业务逻辑。"""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.notes.models import Note
from app.modules.notes.schemas import NoteCreate, NoteUpdate


async def list_notes(db: AsyncSession, page: int = 1, size: int = 20) -> tuple[list[Note], int]:
    total = await db.scalar(select(func.count()).select_from(Note)) or 0
    rows = await db.scalars(
        select(Note).order_by(Note.created_at.desc()).offset((page - 1) * size).limit(size)
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
    await db.commit()
    await db.refresh(note)
    return note


async def delete_note(db: AsyncSession, note: Note) -> None:
    await db.delete(note)
    await db.commit()
