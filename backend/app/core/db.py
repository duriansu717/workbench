"""数据库引擎与会话。

约定：
- 应用内一律使用异步会话（AsyncSession），驱动用 asyncpg
- Alembic 迁移用同一连接串的同步驱动（psycopg）

为什么应用侧不用 psycopg 的异步模式：
psycopg 3 的 async 不支持 Windows 默认事件循环（ProactorEventLoop），
而 uvicorn 不带 --reload 时用的正是它；asyncpg 两者都兼容。
"""

from collections.abc import AsyncGenerator
from datetime import UTC, datetime

from sqlalchemy import DateTime, event
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    ORMExecuteState,
    Session,
    mapped_column,
    with_loader_criteria,
)

from app.core.config import settings


def async_database_url(url: str) -> str:
    """.env 里的连接串以 psycopg 书写（Alembic 用），应用侧统一换成 asyncpg。"""
    for prefix in ("postgresql+psycopg://", "postgresql://"):
        if url.startswith(prefix):
            return "postgresql+asyncpg://" + url[len(prefix) :]
    return url


engine = create_async_engine(
    async_database_url(settings.database_url),
    echo=settings.db_echo,
    pool_pre_ping=True,
)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """所有 ORM 模型的基类。"""


class SoftDeleteMixin:
    """逻辑删除：数据留在库里，只打一个 deleted_at 标记。

    默认查询会自动过滤掉已删除的行（见下面的 do_orm_execute 监听器）；
    需要显式看到它们时，在语句上加 .execution_options(include_deleted=True)。
    """

    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), default=None)

    def soft_delete(self) -> None:
        self.deleted_at = datetime.now(UTC)

    def restore(self) -> None:
        self.deleted_at = None

    @property
    def is_deleted(self) -> bool:
        return self.deleted_at is not None


@event.listens_for(Session, "do_orm_execute")
def _filter_soft_deleted(state: ORMExecuteState) -> None:
    """所有 ORM 查询默认排除逻辑删除的行（SQLAlchemy 官方的软删除配方）。"""
    if (
        state.is_select
        and not state.execution_options.get("include_deleted", False)
        and not state.is_column_load
        and not state.is_relationship_load
    ):
        state.statement = state.statement.options(
            with_loader_criteria(
                SoftDeleteMixin,
                lambda cls: cls.deleted_at.is_(None),
                include_aliases=True,
            )
        )


async def get_db() -> AsyncGenerator[AsyncSession]:
    """FastAPI 依赖：每个请求一个数据库会话。"""
    async with SessionLocal() as session:
        yield session
