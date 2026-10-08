"""跨模块共享的 Pydantic 模型。"""

from pydantic import BaseModel


class Page[T](BaseModel):
    """列表接口统一分页返回：{"items": [...], "total": N}。"""

    items: list[T]
    total: int


class ModuleMeta(BaseModel):
    """功能元信息（GET /api/v1/modules 的返回项，也是前端菜单/宫格的数据源）。"""

    name: str
    title: str
    description: str = ""
    icon: str = ""
    path: str
