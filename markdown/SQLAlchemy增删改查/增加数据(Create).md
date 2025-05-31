# 增加数据(Create)

## 单个创建

### `session.add()`​ 方法

```python
session.add(插入数据)
```

　　**参数说明**:

* ​`instance`​: 要添加的模型实例对象

　　**特点**:

* 将单个对象添加到会话中
* 不会立即执行数据库插入操作
* 需要会话提交(commit)后才会实际写入数据库

### 完整示例

```python
from database import Models

with Models.session_scope() as session:
    # 使用ORM直接创建
    new_app = Models.App(
        name="测试应用1",
        category="测试",
        description="测试描述",
        type="builtin",
        open_command="test.main",
        recommend=True
    )
    session.add(new_app)  # 添加到会话中
```

　　‍

## 多个创建

### `session.add_all()`​ 方法

```python
session.add_all(插入数据)
```

　　**参数说明**:

* ​`instances`​: 包含多个模型实例的可迭代对象(如list)

　　**特点**:

* 批量添加多个对象到会话
* 比多次调用`add()`​更高效
* 同样需要会话提交后才会实际写入

　　‍

### 完整示例

```python
from database import Models

with Models.session_scope() as session:
    # 批量创建多个应用
    apps_to_create = [
        Models.App(
            name="测试应用2",
            category="工具",
            description="测试工具",
            type="builtin",
            open_command="test.tool"
        ),
        Models.App(
            name="测试应用3",
            category="系统",
            description="系统工具",
            type="external",
            open_command="system.exe"
        )
    ]
    session.add_all(apps_to_create)
```
