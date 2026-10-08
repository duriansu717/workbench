"""数据库引擎与会话。

约定：
- 应用内一律使用异步会话（AsyncSession），驱动用 asyncpg
- Alembic 迁移用同一连接串的同步驱动（psycopg）

为什么应用侧不用 psycopg 的异步模式：
psycopg 3 的 async 不支持 Windows 默认事件循环（ProactorEventLoop），
而 uvicorn 不带 --reload 时用的正是它；asyncpg 两者都兼容。
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

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


async def get_db() -> AsyncGenerator[AsyncSession]:
    """FastAPI 依赖：每个请求一个数据库会话。"""
    async with SessionLocal() as session:
        yield session
