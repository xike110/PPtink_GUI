# 查询数据 (Retrieve)

## 查询方法说明

### 基础方法

|方法|描述|返回值|
| ------| ----------------------------| --------------------|
|​`first()`​|返回查询结果的第一条记录|单个模型实例或None|
|​`all()`​|返回所有匹配的记录|包含模型实例的列表|
|​`filter_by()`​|使用关键字参数进行简单过滤|查询对象|
|​`filter()`​|使用表达式进行复杂过滤|查询对象|

### `filter_by()`​ 和 `filter()`​ 的区别

|特性|​`filter_by()`​|​`filter()`​|
| ------| -------------------------------| --------------------------------------------------------|
|**参数类型**|使用关键字参数(key\=value)|使用SQLAlchemy表达式|
|**列引用方式**|直接使用列名|使用`Model.column_name`​或`column()`​|
|**运算符**|只支持等值比较(\=)|支持所有比较运算符(\=\=, !\=, \>, \<等)|
|**链式调用**|可以链式调用|可以链式调用|
|**使用场景**|简单等值查询|复杂条件查询|

　　查询不需要 事务回滚，with Models.session_scope() as session:

## 单条查询

```python
from database import Models

app_db = Models.session.query(Models.App).filter(Models.App.name == "测试应用1").first()
if app_db:
    print(f"按名称查询: {app_db.name}, 类别: {app_db.category}")
else:
    print("未找到名为'测试应用1'的应用")
```

　　‍

## 多条查询

```python
from database import Models

app_db = Models.session.query(Models.App).filter(Models.App.name == "测试应用1").order_by(Models.App.id).all()
for app in app_db:
    print(f"查询到应用: {app.name}, 类别: {app.category}, 描述: {app.description}")

```

　　‍

## 排除查询

```python
from database import Models
app_db = Models.session.query(Models.App).filter(Models.App.name != "测试应用2").all()
for app in app_db:
    print(f"查询到应用: {app.name}, 类别: {app.category}, 描述: {app.description}")

```

　　‍

## 获取所有记录

```python
from database import Models

app_db = Models.session.query(Models.App).all()
for app in app_db:
    print(f"查询到应用: {app.name}, 类别: {app.category}, 描述: {app.description}")
```

　　‍

## 复杂条件查询 (Advanced Filtering)

```python
from database import Models
from sqlalchemy import and_, or_, not_

# 使用 and_
app_db = Models.session.query(Models.App).filter(
    and_(
        Models.App.category == "工具",
        Models.App.rating >= 4.0
    )
).all()

# 使用 or_
app_db = Models.session.query(Models.App).filter(
    or_(
        Models.App.category == "游戏",
        Models.App.category == "娱乐"
    )
).all()

# 使用 in_
app_db = Models.session.query(Models.App).filter(
    Models.App.category.in_(["游戏", "社交", "工具"])
).all()

# 模糊查询
app_db = Models.session.query(Models.App).filter(
    Models.App.name.like("%测试%")
).all()

# 范围查询
from datetime import datetime, timedelta
last_week = datetime.now() - timedelta(days=7)
app_db = Models.session.query(Models.App).filter(
    Models.App.create_time.between(last_week, datetime.now())
).all()
```

　　‍

　　‍

　　‍
