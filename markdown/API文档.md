# PPtink桌面GUI框架 API文档

## 核心模块API

### 1. 配置管理 (utils/conf.py)
```python
class Config:
    def __init__(self):
        # 初始化配置
        pass
    
    def load_config(self):
        # 加载配置文件
        pass
    
    def save_config(self):
        # 保存配置
        pass
```

### 2. 登录界面 (utils/login_gui.py)
```python
class Task:
    def __init__(self, ico=None, banner_img=None, banner_text=None):
        """
        初始化登录界面
        :param ico: 图标路径
        :param banner_img: 横幅图片路径
        :param banner_text: 横幅文本
        """
        pass
    
    def login_main(self):
        """
        启动登录界面
        :return: bool 登录是否成功
        """
        pass
```

### 3. GUI工具类 (utils/gui_tkinter.py)
```python
def show_popup(title, message):
    """
    显示弹出窗口
    :param title: 窗口标题
    :param message: 消息内容
    """
    pass
```

### 4. 主界面 (utils/root_gui.py)
```python
class Task:
    def __init__(self, ico=None, banner_img=None, banner_text=None):
        """
        初始化主界面
        :param ico: 图标路径
        :param banner_img: 横幅图片路径
        :param banner_text: 横幅文本
        """
        pass
    
    def root_main(self):
        """
        启动主界面
        """
        pass
```

### 5. 网络请求 (utils/Request.py)
```python
class Task:
    def __init__(self, headers=None, params=None, url=None):
        """
        初始化网络请求
        :param headers: 请求头
        :param params: 请求参数
        :param url: 请求地址
        """
        pass
    
    def aivideo_ceshi(self):
        """
        测试网络连接
        :return: bool 网络是否正常
        """
        pass
```

## 界面模块API

### 1. WebView界面 (app/WEB界面入口)
```python
def main_init():
    """
    初始化WebView界面
    """
    pass
```

### 2. 原生GUI界面 (app/原生界面入口)
```python
def main_init():
    """
    初始化原生GUI界面
    """
    pass
```

## 配置项说明

### 1. 基础配置
```yaml
config:
  url: "API地址"
  brandname: "品牌名称"
  is_network: true  # 是否检查网络
  op_ad: true  # 是否开启开屏广告
```

### 2. 缓存配置
```python
cache:
  uid: "用户ID"
  token: "认证令牌"
```

## 事件处理

### 1. 登录事件
```python
def on_login_success():
    """
    登录成功回调
    """
    pass

def on_login_failed():
    """
    登录失败回调
    """
    pass
```

### 2. 界面事件
```python
def on_window_close():
    """
    窗口关闭回调
    """
    pass

def on_window_resize():
    """
    窗口大小改变回调
    """
    pass
```

## 错误处理

### 1. 网络错误
```python
def handle_network_error():
    """
    处理网络错误
    """
    pass
```

### 2. 认证错误
```python
def handle_auth_error():
    """
    处理认证错误
    """
    pass
```

## 使用示例

### 1. 初始化配置
```python
from utils import conf

config = conf.Config()
config.load_config()
```

### 2. 创建登录界面
```python
from utils import login_gui

login = login_gui.Task(
    ico="ui/ico/ai.ico",
    banner_img='ui/img/banner.png',
    banner_text='登录'
)
if login.login_main():
    print("登录成功")
```

### 3. 发送网络请求
```python
from utils import Request

request = Request.Task(
    headers={"Content-Type": "application/json"},
    url="https://api.example.com"
)
if request.aivideo_ceshi():
    print("网络正常")
``` 