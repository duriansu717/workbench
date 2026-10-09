"""笔记模块的路由（薄层：参数解析 + 调 service）。

注意：/deleted 必须声明在 /{note_id} **之前**，否则 "deleted" 会被当成 UUID 解析。
"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.schemas import Page
from app.modules.notes import service
from app.modules.notes.schemas import NoteCreate, NoteKind, NoteRead, NoteUpdate

router = APIRouter()

NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="笔记不存在")
EMPTY_TITLE = HTTPException(status_code=422, detail="文章标题不能为空")


@router.get("", response_model=Page[NoteRead], summary="笔记列表（可按类型筛选）")
async def list_notes(
    kind: NoteKind | None = Query(None, description="quick=随手小记，article=文章；不传返回全部"),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Page[NoteRead]:
    notes, total = await service.list_notes(db, kind, page, size)
    return Page(items=[NoteRead.model_validate(n) for n in notes], total=total)


@router.get("/deleted", response_model=Page[NoteRead], summary="回收站（已删除的笔记）")
async def list_deleted_notes(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Page[NoteRead]:
    notes, total = await service.list_notes(db, None, page, size, trash=True)
    return Page(items=[NoteRead.model_validate(n) for n in notes], total=total)


@router.post("", response_model=NoteRead, status_code=status.HTTP_201_CREATED, summary="新建笔记")
async def create_note(payload: NoteCreate, db: AsyncSession = Depends(get_db)) -> NoteRead:
    note = await service.create_note(db, payload)
    return NoteRead.model_validate(note)


@router.get("/{note_id}", response_model=NoteRead, summary="笔记详情")
async def get_note(note_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> NoteRead:
    note = await service.get_note(db, note_id)
    if note is None:
        raise NOT_FOUND
    return NoteRead.model_validate(note)


@router.patch("/{note_id}", response_model=NoteRead, summary="修改笔记（不可改类型）")
async def update_note(
    note_id: uuid.UUID, payload: NoteUpdate, db: AsyncSession = Depends(get_db)
) -> NoteRead:
    note = await service.get_note(db, note_id)
    if note is None:
        raise NOT_FOUND
    if note.kind == "article" and payload.title is not None and not payload.title.strip():
        raise EMPTY_TITLE
    note = await service.update_note(db, note, payload)
    return NoteRead.model_validate(note)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT, summary="删除笔记（逻辑删除）")
async def delete_note(note_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    note = await service.get_note(db, note_id)
    if note is None:
        raise NOT_FOUND
    await service.soft_delete_note(db, note)


@router.post("/{note_id}/restore", response_model=NoteRead, summary="从回收站恢复")
async def restore_note(note_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> NoteRead:
    note = await service.get_note(db, note_id, include_deleted=True)
    if note is None:
        raise NOT_FOUND
    note = await service.restore_note(db, note)
    return NoteRead.model_validate(note)


@router.delete(
    "/{note_id}/purge", status_code=status.HTTP_204_NO_CONTENT, summary="彻底删除（不可恢复）"
)
async def purge_note(note_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    note = await service.get_note(db, note_id, include_deleted=True)
    if note is None:
        raise NOT_FOUND
    await service.purge_note(db, note)
