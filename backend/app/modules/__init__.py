"""功能注册表。

新增一个功能：
1. 在 modules/ 下新建一个包（可复制 notes/ 的结构）
2. 把包名加进下面的 MODULES 列表

路由会自动挂载到 /api/v1/<包名>，前端菜单会从 /api/v1/modules 自动读到。

每个功能包的标准结构：
    router.py    路由（薄：只做参数解析和调用 service）
    schemas.py   Pydantic 入参 / 出参
    models.py    SQLAlchemy 模型
    service.py   业务逻辑（唯一放逻辑的地方）
    registry.py  前端菜单 / 宫格的元信息
"""

MODULES: list[str] = [
    "notes",
]
