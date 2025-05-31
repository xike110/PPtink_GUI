# 删除数据 (Delete)

## 单条删除

```python
from database import Models

# 单个删除
with Models.session_scope() as session:
    app_to_delete = session.query(Models.App).filter(Models.App.name == "测试应用1").first()
    session.delete(app_to_delete)
```

　　‍

## 批量删除

```python
from database import Models
# 批量删除
with Models.session_scope() as session:
    session.query(Models.App).filter(
        Models.App.name == "测试应用1"
    ).delete()
```

　　‍
