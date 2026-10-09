"""笔记模块的业务逻辑。

删除一律是逻辑删除（打 deleted_at 标记），数据留在库里；回收站可以恢复。
默认查询会被 app/core/db.py 的全局过滤器挡掉已删除的行，回收站查询用
execution_options(include_deleted=True) 显式绕过。
"""

import uuid

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.notes.models import Note
from app.modules.notes.schemas import NoteCreate, NoteKind, NoteUpdate


async def list_notes(
    db: AsyncSession,
    kind: NoteKind | None = None,
    page: int = 1,
    size: int = 20,
    *,
    trash: bool = False,
) -> tuple[list[Note], int]:
    """trash=False：正常列表；trash=True：回收站（只看已删除的）。"""
    count_stmt = select(func.count()).select_from(Note)
    list_stmt = select(Note)

    if trash:
        count_stmt = count_stmt.execution_options(include_deleted=True).where(
            Note.deleted_at.is_not(None)
        )
        list_stmt = list_stmt.execution_options(include_deleted=True).where(
            Note.deleted_at.is_not(None)
        )

    if kind:
        count_stmt = count_stmt.where(Note.kind == kind)
        list_stmt = list_stmt.where(Note.kind == kind)

    total = await db.scalar(count_stmt) or 0
    rows = await db.scalars(
        list_stmt.order_by(Note.created_at.desc()).offset((page - 1) * size).limit(size)
    )
    return list(rows), total


async def get_note(
    db: AsyncSession, note_id: uuid.UUID, *, include_deleted: bool = False
) -> Note | None:
    """按 id 取一条。默认看不到已删除的（回收站的恢复/彻底删除要传 include_deleted）。

    注意：这里不能用 db.get() —— 它同样会被全局软删除过滤器挡住，
    必须走显式 select，才能用 execution_options 绕过过滤。
    """
    stmt = select(Note).where(Note.id == note_id)
    if include_deleted:
        stmt = stmt.execution_options(include_deleted=True)
    return await db.scalar(stmt)


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


async def soft_delete_note(db: AsyncSession, note: Note) -> None:
    """逻辑删除：只打标记，数据还在，可以去回收站捞回来。"""
    note.soft_delete()
    await db.commit()


async def restore_note(db: AsyncSession, note: Note) -> Note:
    note.restore()
    await db.commit()
    await db.refresh(note)
    return note


async def purge_note(db: AsyncSession, note: Note) -> None:
    """彻底删除 —— 从数据库里真删，不可恢复。"""
    await db.delete(note)
    await db.commit()
