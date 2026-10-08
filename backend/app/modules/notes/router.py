"""笔记模块的路由（薄层：参数解析 + 调 service）。"""

import uuid

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.schemas import Page
from app.modules.notes import service
from app.modules.notes.schemas import NoteCreate, NoteRead, NoteUpdate

router = APIRouter()

NOT_FOUND = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="笔记不存在")


@router.get("", response_model=Page[NoteRead], summary="笔记列表")
async def list_notes(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> Page[NoteRead]:
    notes, total = await service.list_notes(db, page, size)
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


@router.patch("/{note_id}", response_model=NoteRead, summary="修改笔记")
async def update_note(
    note_id: uuid.UUID, payload: NoteUpdate, db: AsyncSession = Depends(get_db)
) -> NoteRead:
    note = await service.get_note(db, note_id)
    if note is None:
        raise NOT_FOUND
    note = await service.update_note(db, note, payload)
    return NoteRead.model_validate(note)


@router.delete("/{note_id}", status_code=status.HTTP_204_NO_CONTENT, summary="删除笔记")
async def delete_note(note_id: uuid.UUID, db: AsyncSession = Depends(get_db)) -> None:
    note = await service.get_note(db, note_id)
    if note is None:
        raise NOT_FOUND
    await service.delete_note(db, note)
