# 更新数据 (Update)

　　‍

## 单条更新

```python
from database import Models
# 方式一：单条查询并修改
with Models.session_scope() as session:
    retrieved_app = session.query(Models.App).filter(Models.App.name == "测试应用1").first()
    retrieved_app.category = "新分类"
    retrieved_app.description = "新描述"
```

　　‍

## 批量更新多条

```python
from database import Models
# 方式二：批量更新
with Models.session_scope() as session:
    session.query(Models.App).filter(
        Models.App.name == "测试应用1"
    ).update({
        "description": "描述修改",
        "recommend": True
    })

```

　　‍
