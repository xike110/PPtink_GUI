import logging
from typing import Dict, List, Any, Union, Optional

# 组件类型枚举
COMPONENT_TYPES = {
    "TextField": "text",  # 文本输入框
    "PasswordField": "password",  # 密码框
    "IntegerField": "number",  # 数字框
    "DecimalField": "number",  # 浮点数框
    "Textarea": "textarea",  # 文本域
    "FileChooser": "file",  # 文件选择
    "MultiFileChooser": "multifile",  # 多文件选择
    "DirChooser": "directory",  # 目录选择
    "FileSaver": "filesaver",  # 文件保存
    "DateChooser": "date",  # 日期选择
    "TimeChooser": "time",  # 时间选择
    "DateTime": "datetime",  # 日期时间选择框
    "Listbox": "select",  # 列表选择框
    "Dropdown": "dropdown",  # 下拉选择框
    "ColourChooser": "color",  # 颜色选择器
    "BlockCheckbox": "checkbox",  # 复选框
    "SwitchField": "switch",  # 开关组件
    "SliderField": "slider",  # 滑动条
    "RadioGroup": "radio"  # 单选框组
}

# 互斥组类型
GROUP_TYPES = {
    "MutuallyExclusiveGroup": "radio",  # 互斥组，只能选一个
    "ArgumentGroup": "group"  # 普通分组
}


class MenuConfig:
    """
    菜单配置类，对应Gooey的顶级菜单项
    """

    def __init__(self, name: str, help: str, components: List[Dict[str, Any]] = None):
        self.name = name  # 菜单名称
        self.help = help  # 菜单帮助信息
        self.components = components or []  # 组件列表
        self.groups = []  # 分组

    def add_component(self, component: Dict[str, Any]):
        """添加组件到菜单"""
        self.components.append(component)

    def add_group(self, group: Dict[str, Any]):
        """添加分组到菜单"""
        self.groups.append(group)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典，用于传递给前端"""
        return {
            "name": self.name,
            "help": self.help,
            "components": self.components,
            "groups": [g for g in self.groups if g.get("components")],
            "type": "menu"
        }


class GooeyConfig:
    """
    Gooey配置管理器，用于生成类似Gooey的界面配置
    """

    def __init__(self, program_name: str, program_description: str):
        self.program_name = program_name  # 程序名称
        self.program_description = program_description  # 程序描述
        self.menus = []  # 菜单列表
        self.current_menu = None  # 当前活动菜单
        self.current_group = None  # 当前活动分组
        self.navigation_items = []  # 导航项

    def add_menu(self, name: str, help: str) -> MenuConfig:
        """添加一个菜单"""
        menu = MenuConfig(name, help)
        self.menus.append(menu)
        self.current_menu = menu
        # 重置当前分组
        self.current_group = None
        # 添加到导航项
        self.navigation_items.append({"name": name, "type": "menu", "help": help})
        return menu

    def convert_gooey_widget(self, widget_type: str, **options) -> Dict[str, Any]:
        """
        转换Gooey的组件类型为Vue组件类型
        """
        component_type = COMPONENT_TYPES.get(widget_type, "text")
        result = {"type": component_type}

        # 处理特定组件的选项
        if widget_type in ["Dropdown", "Listbox", "RadioGroup", "BlockCheckbox"]:
            if "choices" in options:
                result["options"] = []
                for choice in options["choices"]:
                    result["options"].append({"label": choice, "value": choice})

        # 添加数值限制
        if widget_type == "IntegerField" or widget_type == "DecimalField":
            if "min" in options:
                result["min"] = options["min"]
            if "max" in options:
                result["max"] = options["max"]

        # 处理默认值
        if "default" in options:
            result["default"] = options["default"]

        # 复制其他通用选项
        for key, value in options.items():
            if key not in ["choices", "min", "max", "default"]:
                result[key] = value

        return result

    def add_argument(self, name: str, **kwargs) -> None:
        """
        添加参数，模拟argparse的add_argument方法

        参数:
            name: 参数名称
            metavar: 参数显示名称
            help: 帮助文本
            widget: 组件类型
            choices: 选项列表
            default: 默认值
            required: 是否必填
            validate: 验证方法名
            **kwargs: 其他参数
        """
        if not self.current_menu:
            logging.warning("没有活动菜单，无法添加参数")
            return

        # 从kwargs中提取组件定义
        meta_title = kwargs.get("metavar", name)  # 显示标题
        help_text = kwargs.get("help", "")  # 提示文本
        widget_type = kwargs.get("widget", "TextField")  # 组件类型，默认为文本框
        required = kwargs.get("required", False)  # 是否必填
        validate = kwargs.get("validate", None)  # 提取验证方法名

        # 提取gooey_options
        gooey_options = kwargs.get("gooey_options", {})

        # 构建组件配置
        component = {
            "name": name,
            "title": meta_title,
            "help": help_text,
            "required": required,
            "visible": gooey_options.get("visible", True),
            "full_width": gooey_options.get("full_width", False),
        }

        # 添加验证方法名称
        if validate:
            component["validate"] = validate

        # 合并组件特定选项
        widget_options = self.convert_gooey_widget(
            widget_type,
            choices=kwargs.get("choices", []),
            default=kwargs.get("default", None),
            min=gooey_options.get("min", None),
            max=gooey_options.get("max", None),
        )
        component.update(widget_options)

        # 添加到当前分组或菜单
        if self.current_group is not None:
            # 如果有活动分组，添加到分组中
            self.current_group["components"].append(component)
        else:
            # 否则添加到菜单的直接组件列表中
            self.current_menu.add_component(component)

    def add_argument_group(self, title: str, description: str = "", **kwargs) -> Dict[str, Any]:
        """
        添加参数分组
        """
        gooey_options = kwargs.get("gooey_options", {})

        group = {
            "title": title,
            "description": description,
            "components": [],
            "columns": gooey_options.get("columns", 1),
            "show_border": gooey_options.get("show_border", True),
            "show_underline": gooey_options.get("show_underline", False),
            "type": "group"
        }

        if self.current_menu:
            self.current_menu.add_group(group)
            # 设置当前活动分组
            self.current_group = group

        return group

    def to_dict(self) -> Dict[str, Any]:
        """
        转换配置为字典，用于传递给前端
        """
        result = {
            "program_name": self.program_name,
            "program_description": self.program_description,
            "menus": [menu.to_dict() for menu in self.menus],
            "navigation": self.navigation_items
        }
        return result


# 示例用法
def generate_sample_config() -> Dict[str, Any]:
    """
    生成示例配置，用于测试
    """
    config = GooeyConfig("演示DEMO", "这是一个演示DEMO")
    # --------------------------添加基本输入框分组-------------------------------------
    config.add_argument_group("基本输入框(分组)", description="基本的输入控件", gooey_options={"show_border": True, "columns": 2})

    # 文本输入框
    config.add_argument(
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
    config.add_argument(
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
            "placeholder": "请输入整数"  # 占位文本
        }
    )

    # 浮点数框
    config.add_argument(
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
            "placeholder": "请输入浮点数"  # 占位文本
        }
    )

    # 文本域
    config.add_argument(
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
            "resize": "both"  # none, both, horizontal, vertical
        }
    )

    # 开关组件
    config.add_argument(
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
    config.add_argument(
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
            "disabled": False  # 是否禁用
        }
    )

    # --------------------------下拉分组-------------------------------------
    config.add_argument_group("选择下拉(分组)", gooey_options={"show_border": True, "columns": 2})

    # 多选下拉框
    config.add_argument(
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
    config.add_argument(
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
    config.add_menu("不常用组件", "其他不常用组件")

    # 密码框
    config.add_argument(
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
    config.add_argument_group("文件目录选择框(分组)", gooey_options={"show_border": True, "columns": 2})

    # 单文件选择框
    config.add_argument(
        "--Filepath",
        metavar="单文件选择框",
        help="选择文件夹路径",
        type=str,
        default="./xlsx",
        widget="FileChooser",
        gooey_options={
            "buttonText": "选择文件",  # 按钮文本
            "plain": True,  # 是否为朴素按钮
            "size": "default",  # 大小
            "buttonIcon": "Document",  # 按钮图标
            "disabled": False  # 是否禁用
        }
    )

    # 多文件选择框
    config.add_argument(
        "--allpath",
        metavar="多文件选择框",
        help="选择多个文件夹路径",
        nargs="+",
        widget="MultiFileChooser",
        gooey_options={
            "buttonText": "选择多个文件",  # 按钮文本
            "plain": True,  # 是否为朴素按钮
            "size": "default",  # 大小
            "buttonIcon": "Files",  # 按钮图标
            "disabled": False  # 是否禁用
        }
    )

    # 目录选择框
    config.add_argument(
        "--outputDirectory",
        metavar="目录选择框",
        help="选择文件夹路径",
        type=str,
        default="./output",
        widget="DirChooser",
        gooey_options={
            "buttonText": "选择目录",  # 按钮文本
            "plain": True,  # 是否为朴素按钮
            "size": "default",  # 大小
            "buttonIcon": "Folder",  # 按钮图标
            "disabled": False  # 是否禁用
        }
    )

    # 文件保存框
    config.add_argument(
        "--saveFile",
        metavar="文件保存框",
        help="选择保存文件位置",
        type=str,
        default="./output.txt",
        widget="FileSaver",
        gooey_options={
            "buttonText": "选择保存位置",  # 按钮文本
            "plain": True,  # 是否为朴素按钮
            "size": "default",  # 大小
            "buttonIcon": "Save",  # 按钮图标
            "disabled": False  # 是否禁用
        }
    )

    # --------------------------单选复选分组-------------------------------------
    config.add_argument_group("单选复选(分组)", gooey_options={"show_border": True, "columns": 2})

    # 单选框组
    config.add_argument(
        "--radio",
        metavar="单选框组",
        help="只能选择一个选项",
        choices=["单选1", "单选2", "单选3"],
        default="单选1",
        widget="RadioGroup",
        gooey_options={
            "direction": "horizontal",  # 方向 vertical/horizontal
            "size": "default",  # 大小 large/default/small
            "disabled": False,  # 是否禁用
            "textColor": "#ffffff",  # 文本颜色
            "fill": "#409EFF"  # 填充色
        }
    )

    # 复选框组
    config.add_argument(
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
            "size": "default",  # 大小
            "disabled": False  # 是否禁用
        }
    )

    # --------------------------日期时间分组分组-------------------------------------
    config.add_argument_group("时间日期(分组)", gooey_options={"show_border": True, "columns": 2})

    # 日期选择器
    config.add_argument(
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
    config.add_argument(
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
    config.add_argument(
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
    config.add_argument_group("颜色选择器(分组)", gooey_options={"show_border": True, "columns": 1})

    # 颜色选择器
    config.add_argument(
        "--color",
        metavar="颜色选择器",
        help="选择颜色",
        default="#409EFF",
        widget="ColourChooser",
        gooey_options={
            "showAlpha": True,  # 是否支持透明度选择
            "colorFormat": "hex",  # 颜色格式 hex/rgb/hsl
            "predefine": ["#409EFF", "#67C23A", "#E6A23C", "#F56C6C", "#909399"],  # 预定义颜色
            "size": "default",  # 大小
            "disabled": False  # 是否禁用
        }
    )

    # -------------------------------------------------------------------
    #                   导航-启动服务设置
    # -------------------------------------------------------------------
    # 添加表单组件演示菜单
    config.add_menu("服务设置", "是一个启动服务的设置")
    config.add_argument(
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
            "placeholder": "请输入整数"  # 占位文本
        }
    )
    # 返回当前配置
    return config.to_dict()


# 用于测试的代码
if __name__ == "__main__":
    # 生成并打印示例配置
    import json

    sample_config = generate_sample_config()
    print(json.dumps(sample_config, indent=2, ensure_ascii=False))
