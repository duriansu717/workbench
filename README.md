# workbench · 个人工作台

一个持续迭代的自用工作台：**每加一个功能 = 加一个模块目录**，前端菜单和首页宫格会自动出现，不需要改别的地方。

## 技术栈

| 层 | 选型 |
|---|---|
| 后端 | Python 3.14 · FastAPI · SQLAlchemy 2.1（async + asyncpg）· Alembic · Pydantic v2 |
| 数据库 | PostgreSQL 18 |
| 前端 | Vue 3.5 · Vite 8 · TypeScript · Pinia · Vue Router · Element Plus |
| 运行时管理 | FlyEnv（统一管理 Python / Node / PostgreSQL） |

完整选型理由、目录约定与编码规范见 **[docs/技术栈与架构说明.md](docs/技术栈与架构说明.md)**。

## 快速开始

**后端**

```bash
cd backend
python -m venv .venv && .venv\Scripts\activate      # Windows（用 Python 3.14）
pip install -r requirements.txt
cp .env.example .env                                # 按实际情况改 DATABASE_URL
uvicorn app.main:app --reload                       # 接口文档 http://127.0.0.1:8000/docs
```

**前端**

```bash
cd frontend
pnpm install
pnpm dev                                            # http://localhost:1213
```

## 加一个新功能

1. **后端**：复制 `backend/app/modules/notes/` 为新目录，把包名加进 `app/modules/__init__.py` 的 `MODULES`
2. **数据库**：`alembic revision --autogenerate -m "xxx"` → `alembic upgrade head`
3. **前端**：复制 `frontend/src/features/notes/` 为新目录；需要新类型就 `pnpm gen:api-types`
4. 首页宫格和侧边菜单**自动出现**新功能

## 目录结构

```
workbench/
├─ backend/          # FastAPI 应用（app/core 基础设施 + app/modules 功能模块）
│  └─ data/uploads/  # 上传的图片/音频/视频（不进版本库，备份记得带上）
├─ frontend/         # Vue 应用（src/app 外壳 + src/features 功能 + src/shared 公共）
└─ docs/             # 文档
```

## 媒体

图片 / 音频 / 视频通过 `POST /api/v1/media` 上传（单文件上限 200MB，允许的格式见 `backend/app/core/config.py`），
文件落在 `backend/data/uploads/`，由 `/media` 静态目录提供访问。

正文里就是普通 Markdown —— `![名称](/media/2026/10/xxx.mp4)`，前端按扩展名自动渲染成图片 / 音频播放器 / 视频播放器：

- 编辑器里：工具栏按钮选择文件，或直接**粘贴**（截图）、**拖入**（音频/视频）
- 展示时：列表与详情用同一套渲染，视频支持拖动进度条
