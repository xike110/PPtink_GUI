import logging
# import pystray
import webview
from app.WebDemo.utils import conf
import platform
# import tkinter as tk
import ctypes
import threading
import random
import socket


class Home:
    """
    窗口框架的内置函数大全
    window.load_url(url)：在窗口中加载新 URL。
    window.load_html(content)：将 HTML 内容直接加载到窗口中。
    window.evaluate_js(script)：在窗口中执行 JavaScript 代码并返回结果。
    window.toggle_fullscreen()：在全屏模式和窗口模式之间切换窗口。
    window.resize(width, height)：将窗口大小调整为指定的宽度和高度。
    window.move(x, y)：将窗口移动到指定的 x 和 y 坐标。
    window.hide()：隐藏窗口。
    window.show()：如果窗口处于隐藏状态，则显示该窗口。
    window.minimize()：最小化窗口。
    window.restore()：如果窗口最小化或最大化，则恢复窗口。
    window.destroy()：关闭窗口。
    """

    def __init__(self):
        self.icon = None  # 托盘窗口
        self.sign = conf.SIGN  # 窗口标识
        self.window_isview = True  # 窗口是否显示
        self.autostart = 1  # 是否自动启动 0:开机启动 1:手动启动
        self.theme = "light"  # 主题 light=浅色 dark=深色
        self.main = None  # 入口地址
        self.windows = []  # 窗口对象
        self.father_data = None  # 父窗口传递进来的数据
        self.formdata = None  # 开机启动的数据
        self.runstate = False  # 运行状态

    def title(self) -> str:
        """
        获取或设置窗口的标题-动作
        """

        return self.windows[0].title

    def on_top(self) -> bool:
        """
        获取或设置窗口是否始终位于顶部-动作
        """

        return self.windows[0].on_top

    def x(self) -> int:
        """
        获取窗口左上角的 X 坐标-动作
        """

        return self.windows[0].x

    def y(self) -> int:
        """
        获取窗口左上角的 Y 坐标。-动作
        """

        return self.windows[0].y

    def width(self) -> int:
        """
        获取窗口的宽度-动作
        """

        return self.windows[0].width

    def height(self) -> int:
        """
        获取窗口的高度-动作
        """

        return self.windows[0].height

    def clear_cookies(self) -> None:
        """
        清除窗口中的所有 cookies-动作
        """

        self.windows[0].clear_cookies()  # 清除窗口中的所有 cookies

    def minimize(self):
        """
        最小化窗口-动作
        """
        self.windows[0].minimize()  # 最小化窗口

    def destroy(self):
        """
        关闭窗口-动作
        """
        self.log("info", F"{self.sign}应用窗口已关闭")
        self.windows[0].destroy()  # 关闭窗口

    def restore(self):
        """
        还原窗口-动作
        """

        self.windows[0].restore()

    def resize(self, width, height):
        """
        调整窗口大小-动作
        """

        self.windows[0].resize(width, height)

    def move(self, x, y):
        """
        移动窗口-动作
        """

        self.windows[0].move(x, y)

    def get_taskbar_height(self):
        """
        获取当前系统任务栏的高度。

        该函数通过调用Windows API来查找任务栏窗口，并获取其矩形区域。根据任务栏的位置（底部、右侧、顶部或左侧），
        计算任务栏的高度或宽度，并返回一个合理的任务栏高度值。

        返回值:
            int: 任务栏的高度。如果无法找到任务栏窗口，则返回默认值40。
        """
        hwnd = ctypes.windll.user32.FindWindowW("Shell_TrayWnd", None)

        if hwnd:
            # 获取任务栏的矩形区域
            rect = ctypes.wintypes.RECT()
            ctypes.windll.user32.GetWindowRect(hwnd, ctypes.byref(rect))

            # 根据任务栏的位置计算高度或宽度
            if rect.top > 0:  # 任务栏在底部
                taskbar_height = rect.bottom - rect.top
            elif rect.left > 0:  # 任务栏在右侧
                taskbar_height = rect.right - rect.left
            else:  # 任务栏在顶部或左侧
                taskbar_height = max(rect.bottom - rect.top, rect.right - rect.left)

            # 记录任务栏的位置和计算出的尺寸
            # self.log("info",f'任务栏位置: 左{rect.left}, 上{rect.top}, 右{rect.right}, 下{rect.bottom}')
            # self.log("info",f'计算出的任务栏尺寸: {taskbar_height}')

            # 对计算出的任务栏高度进行合理性调整-防止,返回高于100或低于10
            taskbar_height = max(30, min(48, taskbar_height)) if 10 <= taskbar_height <= 100 else 40

            return taskbar_height
        else:
            # 如果无法找到任务栏窗口，记录警告并返回默认值
            self.log("warning", "无法找到任务栏窗口")
            return 40

    def get_theme(self):
        """
        获取当前主题设置
        
        返回值:
            str: 主题类型，'light'表示浅色主题，'dark'表示深色主题
        """
        return self.theme

    def toggle_fullscreen(self):
        """
        切换全屏模式和窗口模式-动作
        """
        window = self.windows[0]  # 获取窗口对象
        screens = webview.screens
        self.log("info", f'屏幕尺寸:{screens}')
        # 获取当前操作系统的名称
        system_name = platform.system()

        # 判断是否为 Windows 操作系统
        if system_name == "Windows":
            if window.fullscreen:
                self.log("info", '切换到窗口模式')
                window.resize(conf.GUI_POWER[0], conf.GUI_POWER[1])
                # 移动到上下居中
                window.move(
                    (screens[0].width - window.width) // 2,
                    (screens[0].height - window.height) // 2
                )
                window.fullscreen = False
            else:
                self.log("info", '切换到最大化模式')
                # window.toggle_fullscreen()
                # 不使用原生全屏，而是使用调整大小和位置的方式实现最大化效果
                # 计算底部工具栏的高度（通常为30像素）
                taskbar_height = self.get_taskbar_height()  # 获取底部工具栏高度
                # 获取屏幕宽高
                screen_width = screens[0].width
                screen_height = screens[0].height
                # 调整窗口大小为屏幕宽度和屏幕高度减去任务栏高度
                window.resize(screen_width, screen_height - taskbar_height)
                # 移动窗口到屏幕左上角位置
                window.move(0, 0)
                window.fullscreen = True
        # 判断是否为 Linux 操作系统
        elif system_name == "Linux":
            window.toggle_fullscreen()
        # 判断是否为 macOS 操作系统
        elif system_name == "Darwin":
            window.toggle_fullscreen()
        else:
            window.toggle_fullscreen()

    def show(self):
        """
        显示窗口-动作
        """

        self.windows[0].show()

    def hide(self, ):
        """
        隐藏窗口-动作
        """

        self.windows[0].hide()

    def on_closed(self):
        """
        窗口事件监听
        """
        # self.log("info", "应用窗口已关闭")
        pass

    def on_closing(self):
        """
        窗口事件监听
        """
        self.log("info", '应用窗口正在关闭')
        # 终止正在运行的线程
        if self.runstate:
            self.log("info", f"检测到窗口关闭，正在终止{self.sign}_task线程")
            # 将运行状态设置为False
            self.runstate = False
            # 获取所有线程
            for thread in threading.enumerate():
                # 查找指定名称的线程
                if thread.name == f"{self.sign}_task" and thread.is_alive():
                    try:
                        # 使用ctypes终止线程
                        raise_exception_in_thread = ctypes.pythonapi.PyThreadState_SetAsyncExc
                        thread_id = ctypes.c_long(thread.ident)
                        exception = ctypes.py_object(SystemExit)
                        raise_exception_in_thread(thread_id, exception)
                        self.log("info", f"成功终止{self.sign}_task线程")
                    except Exception as e:
                        self.log("error", f"终止{self.sign}_task线程失败: {str(e)}")
        pass

    def on_shown(self):
        """
        窗口事件监听
        """
        self.log("info", '显示应用窗口')
        # if self.father_data.get("bkgrdstat"):
        #     self.log("info", '后台运行')
        #     self.windows[0].hide()  # 隐藏窗口

    def on_minimized(self):
        """
        窗口事件监听
        """
        # self.log("info",'应用窗口最小化')
        pass

    def on_restored(self):
        """
        窗口事件监听
        """
        # self.log("info",'应用窗口已还原')
        pass

    def on_maximized(self):
        """
        窗口事件监听
        """
        # self.log("info",'应用窗口已最大化')
        pass

    def on_loaded(self):
        """
        窗口事件监听
        """
        # self.log("info",'DOM已准备就绪')
        pass

    def on_resized(self, width, height):
        """
        窗口事件监听
        """
        # self.log("info",'应用窗口已调整大小。新的维度是 {width} x {height}'.format(width=width, height=height))
        pass

    def on_moved(self, x, y):
        """
        窗口事件监听-窗口位置改变事件
        """
        pass

    def open_file_dialog(self):
        """
        打开文件选择对话框并返回选择的文件路径
        """
        # 获取当前窗口
        file_path = self.windows[0].create_file_dialog(webview.OPEN_DIALOG)
        return file_path[0] if file_path else "未选择文件"

    def open_multiple_files_dialog(self):
        """
        打开多文件选择对话框并返回选择的所有文件路径
        """
        files_path = self.windows[0].create_file_dialog(webview.OPEN_DIALOG, allow_multiple=True)
        return files_path if files_path else []

    def open_directory_dialog(self):
        """
        打开目录选择对话框并返回选择的目录路径
        """
        # 获取当前窗口
        dir_path = self.windows[0].create_file_dialog(webview.FOLDER_DIALOG)
        return dir_path[0] if dir_path else "未选择目录"

    def notify(self, title="我是标题", message="我是消息类容"):
        """
        通知
        title: 标题
        message: 消息
        """
        self.icon.notify(
            title=title,  # 通知标题
            message=message,  # 通知内容
        )  # 通知

    def log(self, tpre_str="info", value=None):
        """
        调试日志
        参数:
            tpre_str: 日志级别或日志内容
            value: 日志内容，可为None
        
        函数适应两种调用方式:
        1. log("info", "消息内容")   - 标准调用
        2. log("消息内容", "info")   - 参数顺序颠倒的情况
        """
        log_levels = ["info", "error", "warning", "debug", "critical"]

        # 确定日志级别和内容
        if value is None:
            # 仅提供一个参数的情况，默认为info级别
            log_level = "info"
            content = tpre_str
        elif tpre_str in log_levels:
            # 第一个参数是日志级别的标准情况
            log_level = tpre_str
            content = value
        elif value in log_levels:
            # 参数顺序颠倒的情况
            log_level = value
            content = tpre_str
        else:
            # 两个参数都不是标准日志级别的情况
            log_level = "info"
            content = f"{tpre_str}: {value}"

        # 根据确定的日志级别记录日志
        if log_level == "info":
            logging.info(f"{self.sign}: {content}")
        elif log_level == "error":
            logging.error(f"{self.sign}: {content}")
        elif log_level == "warning":
            logging.warning(f"{self.sign}: {content}")
        elif log_level == "debug":
            logging.debug(f"{self.sign}: {content}")
        elif log_level == "critical":
            logging.critical(f"{self.sign}: {content}")

    def get_runstate(self):
        """
        获取运行状态
        """
        return self.runstate

    def set_runstate(self, state: bool):
        """
        设置运行状态
        """
        self.runstate = state

    def get_screen_size(self):
        """获取屏幕尺寸，减去任务栏高度"""
        user32 = ctypes.windll.user32
        screen_width = user32.GetSystemMetrics(0)  # 屏幕宽度
        screen_height = user32.GetSystemMetrics(1)  # 屏幕高度
        taskbar_height = user32.GetSystemMetrics(4)  # 任务栏高度(Windows任务栏默认高度)
        return screen_width, screen_height - taskbar_height

    def get_random_unused_port(self, min_port=1024, max_port=65535):
        """
        获取一个未被占用的随机端口号

        参数:
            min_port (int): 最小端口号，默认为1024（0-1023为系统保留端口）
            max_port (int): 最大端口号，默认为65535

        返回:
            int: 未被占用的随机端口号
        """
        while True:
            # 生成随机端口号
            port = random.randint(min_port, max_port)

            # 检查端口是否被占用
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(('0.0.0.0', port))
                    # 如果bind成功，说明端口未被占用
                    return port
                except socket.error:
                    # 端口被占用，继续循环
                    continue
