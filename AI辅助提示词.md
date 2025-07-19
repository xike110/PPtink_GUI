# AI 辅助提示词

## 主程序入口
运行主程序入口：`main.py`

## 核心配置文件
- `app/WebDemo/utils/conf.py`: 配置文件，用于控制界面 GUI 的显示与交互。
  - 编写使用帮助请修改 `conf.py` 的 `ASKED_QUESTIONS`。
  - 编写软件介绍请修改 `conf.py` 的 `ABOUTUS`。
- `config/config.yaml`: 配置文件，可添加后端非交互执行的参数和默认参数，并添加到界面交互组件的 `default` 配置中。

## 业务逻辑文件
- `app/WebDemo/RunCode.py`: 如果存在演示代码，请先删除演示的界面交互组件代码（范围从第67行-482行），在此文件编写生成界面的代码与传参。
- `app/WebDemo/services/RunTask.py`: 编写接收参数的具体业务逻辑代码并返回结果，控制进度条等待。`def process_args(self, args):` 是示例代码。
- `app/WebDemo/common/validate.py`: 编写验证函数，带入到生成界面交互组件代码的 `validate` 参数中。前端提交时会显示红色提示，提供参数格式约束提示等，后端接收时也会同步验证。

## 数据相关
- `database/Models.py`: 数据库文件，如果需要持久化存储，可在此文件中添加数据库表。`markdown/SQLAlchemy增删改查/` 是数据增删改查文档目录，可供阅读。

## 其他工具与功能
- `utils/gui_tkinter.py`: Tkinter 原生交互组件代码，执行过程中需要弹出原生交互界面可在此文件编写。
- `utils/Request.py`: 请求封装文件，如果需要调用接口，可在此文件编写接口请求代码。
- `log/`: 日志目录，可查看最新日期名称的日志文件，获取错误日志。
- **缓存**: 开发过程中如果需要缓存，已安装 `diskcache` 缓存。使用方法：导入 `from app.WebDemo.utils import conf`，使用 `conf.cache.get('缓存KEY', None)`。

## 开发流程建议
- `首先配置conf.py中的界面文本
- `在RunCode.py中设计界面组件
- `在validate.py中添加参数验证规则
- `在RunTask.py中实现业务逻辑
- `如需持久化，修改Models.py并参考SQLAlchemy文档
- `通过日志系统调试和排查问题

## 生成界面交互组件代码示例
以下是生成界面交互组件的代码示例（根据需要添加）：

```Python
# 添加表单组件演示菜单
self.gui_config.add_menu("常用组件", "是一个组常用框体演示")
# --------------------------添加基本输入框分组-------------------------------------
self.gui_config.add_argument_group("基本输入框(分组)", description="分组描述", gooey_options={"show_border": True, "columns": 1})

# 文本输入框
self.gui_config.add_argument(
    "name",
    metavar="文本输入框",
    help="输入字符串",
    default="小云",
    widget="TextField",
    validate="customize_verify",
    gooey_options={
        "placeholder": "请输入您的名称",  # 占位文本
        "maxlength": 50,  # 最大长度
        "minlength": 2,  # 最小长度
        "readonly": False,  # 是否只读
        "disabled": False,  # 是否禁用
        "clearable": True,  # 是否可清空
        "showWordLimit": True,  # 是否显示字数限制
        "prefixIcon": "User",  # 前缀图标
        "size": "large"  # 大小 large/default/small
    },
)

# 数字整数框
self.gui_config.add_argument(
    "integer",
    metavar="数字整数框",
    help="只能输入整数",
    type=int,
    default=1,
    widget="IntegerField",
    validate="integer_verify",
    gooey_options={
        "min": 0,  # 最小值
        "max": 100,  # 最大值
        "step": 1,  # 步长
        "stepStrictly": False,  # 是否只能输入步长的倍数
        "controls": True,  # 是否显示控制按钮
        "controlsPosition": "right",  # 控制按钮位置
        "placeholder": "请输入整数",  # 占位文本
        "size": "large"
    }
)

# 浮点数框
self.gui_config.add_argument(
    "decimal",
    metavar="数字浮点框",
    help="只能输入浮点数",
    default=0.1,
    widget="DecimalField",
    gooey_options={
        "min": -5.0,  # 最小值
        "max": 5.0,  # 最大值
        "step": 0.1,  # 步长
        "precision": 2,  # 精度，小数位数
        "controls": True,  # 是否显示控制按钮
        "placeholder": "请输入浮点数",  # 占位文本
        "size": "large"

    }
)

# 文本域
self.gui_config.add_argument(
    "texts",
    metavar="超文本框",
    help="输入超文本",
    default="这是一段介绍",
    widget="Textarea",
    gooey_options={
        "height": 100,  # 高度
        "width": 200,  # 宽度
        "readonly": False,  # 是否只读
        "autosize": {"minRows": 3, "maxRows": 6},  # 自动调整大小
        "maxlength": 500,  # 最大长度
        "showWordLimit": True,  # 是否显示字数限制
        "placeholder": "请输入详细描述",  # 占位文本
        "resize": "both",  # none, both, horizontal, vertical
        "size": "large"
    }
)

# 开关组件
self.gui_config.add_argument(
    "switch",
    metavar="开关组件",
    help="切换开关状态",
    default=True,
    widget="SwitchField",
    gooey_options={
        "activeValue": True,  # 打开时的值
        "inactiveValue": False,  # 关闭时的值
        "activeText": "开启",  # 打开时的文字
        "inactiveText": "关闭",  # 关闭时的文字
        "activeColor": "#13ce66",  # 打开时的颜色
        "inactiveColor": "#ff4949",  # 关闭时的颜色
        "width": 60,  # 宽度
        "size": "large",  # 大小
        "inlinePrompt": False,  # 是否在按钮中显示文字
        "disabled": False  # 是否禁用
    }
)

# 滑块组件
self.gui_config.add_argument(
    "--slider",
    metavar="滑块组件",
    help="拖动滑块选择值",
    default=50,
    widget="SliderField",
    gooey_options={
        "min": 0,  # 最小值
        "max": 100,  # 最大值
        "step": 1,  # 步长
        "showInput": True,  # 是否显示输入框
        "showStops": False,  # 是否显示间断点
        "showTooltip": True,  # 是否显示提示
        "range": False,  # 是否为范围选择
        "vertical": False,  # 是否垂直模式
        "height": "200px",  # 高度
        "marks": {0: "0%", 25: "25%", 50: "50%", 75: "75%", 100: "100%"},  # 标记点
        "disabled": False,  # 是否禁用
        "size": "large"
    }
)

# --------------------------下拉分组-------------------------------------
self.gui_config.add_argument_group("选择下拉(分组)", description="分组描述", gooey_options={"show_border": True, "columns": 1})

# 多选下拉框
self.gui_config.add_argument(
    "--filteroption",
    metavar="多选下拉",
    help="选择要筛选数据的列名",
    choices=["选项一", "选项二", "选项三", "选项四", "选项五"],
    required=True,
    widget="Listbox",
    nargs="*",
    default=["选项一", "选项二"],
    gooey_options={
        "full_width": True,  # 是否占满宽度
        "height": 100,  # 高度
        "filterable": True,  # 是否可搜索
        "collapseTags": True,  # 是否折叠标签
        "collapseTagsTooltip": True,  # 是否在折叠标签时显示tooltip
        "placeholder": "请选择多个选项",  # 占位文本
        "multipleLimit": 0,  # 0表示不限制
        "size": "large"  # 大小
    }
)

# 单选下拉框
self.gui_config.add_argument(
    "--dropdownbox",
    metavar="单选下拉框",
    help="选择你需要的",
    choices=["选择一", "选择二", "选项三", "选项四", "选项五"],
    default="选择一",
    widget="Dropdown",
    gooey_options={
        "filterable": True,  # 是否可搜索
        "placeholder": "请选择一个选项",  # 占位文本
        "clearable": True,  # 是否可清空
        "remote": False,  # 是否为远程搜索
        "loading": False,  # 是否加载中
        "loadingText": "加载中...",  # 加载中文本
        "noMatchText": "无匹配数据",  # 无匹配文本
        "noDataText": "无数据",  # 无数据文本
        "reserveKeyword": True,  # 是否保留搜索关键字
        "size": "large"  # 大小
    }
)

# -------------------------------------------------------------------
#                   导航-其他组件
# -------------------------------------------------------------------
# 添加组合布局演示菜单
self.gui_config.add_menu("不常用组件", "其他不常用组件")

# 密码框
self.gui_config.add_argument(
    "password",
    metavar="密码框",
    help="输入密码",
    default="123456",
    widget="PasswordField",
    gooey_options={
        "showPassword": True,  # 是否显示密码切换按钮
        "placeholder": "请输入密码",  # 占位文本
        "clearable": True,  # 是否可清空
        "maxlength": 20,  # 最大长度
        "minlength": 6,  # 最小长度
        "size": "large",  # 大小
        "prefixIcon": "Lock",  # 前缀图标
        "autocomplete": "off"  # 自动完成
    }
)

# --------------------------文件目录选择框分组-------------------------------------
self.gui_config.add_argument_group("文件目录选择框(分组)", description="分组描述", gooey_options={"show_border": True, "columns": 1})

# 单文件选择框
self.gui_config.add_argument(
    "--Filepath",
    metavar="单文件选择框",
    help="选择文件夹路径",
    type=str,
    default="./xlsx",
    widget="FileChooser",
    gooey_options={
        "buttonText": "选择文件",  # 按钮文本
        "plain": True,  # 是否为朴素按钮
        "size": "large",  # 大小
        "buttonIcon": "Document",  # 按钮图标
        "disabled": False  # 是否禁用
    }
)

# 多文件选择框
self.gui_config.add_argument(
    "--allpath",
    metavar="多文件选择框",
    help="选择多个文件夹路径",
    nargs="+",
    widget="MultiFileChooser",
    gooey_options={
        "buttonText": "选择多个文件",  # 按钮文本
        "plain": True,  # 是否为朴素按钮
        "size": "large",  # 大小
        "buttonIcon": "Files",  # 按钮图标
        "disabled": False  # 是否禁用
    }
)

# 目录选择框
self.gui_config.add_argument(
    "--outputDirectory",
    metavar="目录选择框",
    help="选择文件夹路径",
    type=str,
    default="./output",
    widget="DirChooser",
    gooey_options={
        "buttonText": "选择目录",  # 按钮文本
        "plain": True,  # 是否为朴素按钮
        "size": "large",  # 大小
        "buttonIcon": "Folder",  # 按钮图标
        "disabled": False  # 是否禁用
    }
)

# 文件保存框
self.gui_config.add_argument(
    "--saveFile",
    metavar="文件保存框",
    help="选择保存文件位置",
    type=str,
    default="./output.txt",
    widget="FileSaver",
    gooey_options={
        "buttonText": "选择保存位置",  # 按钮文本
        "plain": True,  # 是否为朴素按钮
        "size": "large",  # 大小
        "buttonIcon": "Save",  # 按钮图标
        "disabled": False  # 是否禁用
    }
)

# --------------------------单选复选分组-------------------------------------
self.gui_config.add_argument_group("单选复选(分组)", description="分组描述", gooey_options={"show_border": True, "columns": 1})

# 单选框组
self.gui_config.add_argument(
    "--radio",
    metavar="单选框组",
    help="只能选择一个选项",
    choices=["单选1", "单选2", "单选3"],
    default="单选1",
    widget="RadioGroup",
    gooey_options={
        "direction": "horizontal",  # 方向 vertical/horizontal
        "size": "large",  # 大小 large/default/small
        "disabled": False,  # 是否禁用
        "textColor": "#ffffff",  # 文本颜色
        "fill": "#409EFF"  # 填充色
    }
)

# 复选框组
self.gui_config.add_argument(
    "--checkbox",
    metavar="复选框组",
    help="可以选择多个选项",
    choices=["复选1", "复选2", "复选3"],
    default=["复选1", "复选2"],
    widget="BlockCheckbox",
    gooey_options={
        "direction": "vertical",  # 方向 vertical/horizontal
        "min": 1,  # 最少选择数量
        "max": 2,  # 最多选择数量
        "size": "large",  # 大小
        "disabled": False  # 是否禁用
    }
)

# --------------------------日期时间分组分组-------------------------------------
self.gui_config.add_argument_group("时间日期(分组)", description="分组描述", gooey_options={"show_border": True, "columns": 1})

# 日期选择器
self.gui_config.add_argument(
    "--date",
    metavar="日期",
    help="选择日期",
    default="2024-06-14",
    widget="DateChooser",
    gooey_options={
        "dateType": "date",  # 日期类型 date/dates/week/month/year/years
        "format": "YYYY-MM-DD",  # 格式化
        "valueFormat": "YYYY-MM-DD",  # 值格式化
        "placeholder": "选择日期",  # 占位文本
        "clearable": True,  # 是否可清空
        "editable": True,  # 是否可编辑
        "size": "large",  # 大小
        "disabled": False  # 是否禁用
    }
)

# 时间选择器
self.gui_config.add_argument(
    "--time",
    metavar="时间",
    help="选择时间",
    default="13:14:22",
    widget="TimeChooser",
    gooey_options={
        "format": "HH:mm:ss",  # 格式化
        "valueFormat": "HH:mm:ss",  # 值格式化
        "placeholder": "选择时间",  # 占位文本
        "clearable": True,  # 是否可清空
        "editable": True,  # 是否可编辑
        "size": "large",  # 大小
        "disabled": False,  # 是否禁用
        "isRange": False,  # 是否为范围选择
        "arrowControl": True  # 是否使用箭头进行时间选择
    }
)

# 日期时间选择器
self.gui_config.add_argument(
    "--datetime",
    metavar="日期时间",
    help="选择日期时间",
    default="2024-06-14 13:14:22",
    widget="DateTime",
    gooey_options={
        "dateTimeType": "datetime",  # 日期时间类型 datetime/datetimerange
        "format": "YYYY-MM-DD HH:mm:ss",  # 格式化
        "valueFormat": "YYYY-MM-DD HH:mm:ss",  # 值格式化
        "placeholder": "选择日期和时间",  # 占位文本
        "clearable": True,  # 是否可清空
        "editable": True,  # 是否可编辑
        "size": "large",  # 大小
        "disabled": False  # 是否禁用
    }
)

# --------------------------添加颜色选择器-------------------------------------
self.gui_config.add_argument_group("颜色选择器(分组)", description="分组描述", gooey_options={"show_border": True, "columns": 1})

# 颜色选择器
self.gui_config.add_argument(
    "--color",
    metavar="颜色选择器",
    help="选择颜色",
    default="#409EFF",
    widget="ColourChooser",
    gooey_options={
        "showAlpha": True,  # 是否支持透明度选择
        "colorFormat": "hex",  # 颜色格式 hex/rgb/hsl
        "predefine": ["#409EFF", "#67C23A", "#E6A23C", "#F56C6C", "#909399"],  # 预定义颜色
        "size": "large",  # 大小
        "disabled": False  # 是否禁用
    }
)

# -------------------------------------------------------------------
#                   导航-启动服务设置
# -------------------------------------------------------------------
# 添加表单组件演示菜单
self.gui_config.add_menu("服务设置", "是一个启动服务的设置")
self.gui_config.add_argument(
    "port",
    metavar="服务端口",
    help="输入启动服务的端口",
    type=int,
    default=8080,
    widget="IntegerField",
    gooey_options={
        "min": 0,  # 最小值
        "max": 10000,  # 最大值
        "step": 1,  # 步长
        "stepStrictly": False,  # 是否只能输入步长的倍数
        "controls": True,  # 是否显示控制按钮
        "controlsPosition": "right",  # 控制按钮位置
        "placeholder": "请输入整数",  # 占位文本
        "size": "large"

    }
)
# 返回当前配置
return self.gui_config.to_dict()
```
