"""应用入口。

新增功能不需要改这里的代码：把功能包名加进 app/modules/__init__.py 的
MODULES 列表即可，路由会自动挂载到 /api/v1/<功能名>。
"""

from importlib import import_module

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.schemas import ModuleMeta
from app.modules import MODULES

app = FastAPI(title=settings.app_name, debug=settings.debug)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for _name in MODULES:
    _router = import_module(f"app.modules.{_name}.router").router
    app.include_router(_router, prefix=f"/api/v1/{_name}", tags=[_name])


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok", "app": settings.app_name}


@app.get("/api/v1/modules", response_model=list[ModuleMeta], tags=["system"])
async def list_modules() -> list[ModuleMeta]:
    """工作台首页宫格 / 菜单的数据源：返回所有已注册功能的元信息。"""
    items: list[ModuleMeta] = []
    for name in MODULES:
        meta = getattr(import_module(f"app.modules.{name}.registry"), "META", {})
        items.append(ModuleMeta(name=name, **meta))
    return items
