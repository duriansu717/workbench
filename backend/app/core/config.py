"""应用配置：统一从 .env 读取，全局通过 settings 访问。"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# backend/ 目录（本文件位于 backend/app/core/config.py）
BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "workbench"
    debug: bool = True

    # 数据库连接串：同一个 URL 同时服务异步应用和同步 Alembic（psycopg 3 双模）
    database_url: str = "postgresql+psycopg://postgres:REPLACE_ME@127.0.0.1:5432/workbench"
    db_echo: bool = False

    secret_key: str = "dev-secret-change-me"

    # 前端开发服务器来源（前端固定跑在 1213）
    cors_origins: list[str] = ["http://localhost:1213", "http://127.0.0.1:1213"]


settings = Settings()
