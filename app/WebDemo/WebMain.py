import logging
import bottle
import webview
import os
from app.WebDemo.RunCode import RunCode
from app.WebDemo.utils import conf

main_str = f"{__name__}.main_init()"  # 返回给配置文件路径


def main_init(windows=None, icon=None, father_data=None, autostart=1, formdata=None):
    """
    独立窗口初始化函数
    """

    # 如果没有传入father_data，创建默认的配置
    if father_data is None:
        father_data = {"theme": "default"}

    # logging.info(f"窗口数量:{windows}")  # 打印

    # logging.info(f"子窗口路径：{conf.DIST_DIR}")
    api = RunCode()  # 创建互调件对象
    # api.icon = icon  # 托盘窗口
    api.autostart = autostart  # 启动状态
    api.theme = father_data.get("theme", "default")  # 主题，提供默认值
    api.main = main_str  # 返回给配置文件路径
    # api.father_data = father_data  # 父窗口数据
    # api.formdata = formdata  # 开机启动参数
    api.log(f"开机启动参数值: {api.formdata}")

    # 计算适合的窗口尺寸
    fullscreen, window_width, window_height = (False, *api.get_screen_size()) if conf.GUI_FULLSCREENSTARTUP else (False, conf.GUI_POWER[0], conf.GUI_POWER[1])
    api.windows.append(webview.create_window(
        # -------所有参数------
        # title- 窗口标题
        # url- 要加载的 URL。如果 URL 没有协议前缀，则会将其解析为相对于应用程序入口点的路径。或者，可以传递 WSGI 服务器对象来启动本地 Web 服务器。
        # html- 要加载的 HTML 代码。如果同时指定了 URL 和 HTML，则 HTML 优先。
        # js_api- 将 python 对象暴露给当前窗口的 DOM。可以通过调用 从 Javascript 执行对象的方法。请注意，调用 Javascript 函数会收到一个 Promise，该 Promise 将包含 python 函数的返回值。只有基本的 Python 对象（如 int、str、dict 等）可以返回到 Javascript。桌面js_apiwindows[1].桌面.api.<methodname>(<parameters>)
        # width- 窗口宽度。默认值为 800px。
        # height- 窗口高度。默认值为 600px。
        # x- 窗口 x 坐标。默认值为 centered。
        # y- 窗口 y 坐标。默认值为 centered。
        # resizable- 是否可以调整窗口大小。默认值为 True
        # fullscreen- 以全屏模式启动。默认值为 False
        # min_size- 一个 （width， height） 元组，用于指定最小窗口大小。默认值为 200x100
        # hidden- 创建一个默认隐藏的窗口。默认值为 False
        # frameless- 创建无框窗口。默认值为 False。
        # easy_drag- 无框窗口的轻松拖动模式。可以通过拖动任何点来移动窗口。默认值为 True。请注意，easy_drag 对普通窗口没有影响。要基于元素控制拖动，请参阅拖动区域了解详细信息。
        # minimized- 以最小化模式启动
        # on_top- 将 window 设置为始终位于其他窗口之上。默认值为 False。
        # confirm_close- 是否显示窗口关闭确认对话框。默认值为 False
        # background_color- 加载 WebView 之前显示的窗口的背景颜色。指定为十六进制颜色。默认值为 white。
        # transparent- 创建一个透明窗口。在 Windows 上不受支持。默认值为 False。请注意，此设置不会隐藏窗口镶边或使其透明。要隐藏窗口镶边，请设置为 True。frameless
        # text_select- 启用文档文本选择。默认值为 False。要基于每个元素控制文本选择，请使用用户选择 （打开新窗口）CSS 属性。
        title=f'{conf.GUI_NAME}',  # 窗口标题
        url=conf.DIST_DIR,
        # url=os.path.join(os.path.join(os.path.dirname(__file__)), 'index.html'),  # 窗口加载的html文件
        width=window_width,  # 窗口宽度
        height=window_height,  # 窗口高度
        js_api=api,  # 创建互调件对象
        fullscreen=fullscreen,  # 是否使用全屏模式
        frameless=conf.HEADER,  # 创建无框窗口。默认值为 False。 如果使用无框 pywebview 窗口，可以在 html <div class='pywebview-drag-region'>标签嵌套最外层，实现拖动窗口</div>
        confirm_close=True,  # 是否显示窗口关闭确认对话框。默认值为 False
        resizable=True,  # 是否启用是调整窗口大小和最大化。默认值为 True
        focus=True,  # 窗口是否自动获取焦点。默认值为 True
    ))
    # logging.info(webview.settings)
    # ------webview.settings 参数--------
    # 'ALLOW_DOWNLOADS': False 允许下载：关闭（不允许下载）
    # 'ALLOW_FILE_URLS': True 允许文件URL：开启（允许使用文件URL）
    # 'OPEN_EXTERNAL_LINKS_IN_BROWSER': True 在浏览器中打开外部链接：开启（外部链接将在浏览器中打开）
    # 'OPEN_DEVTOOLS_IN_DEBUG': True 调试时打开开发者工具：开启（在调试模式下自动打开开发者工具）
    # 'REMOTE_DEBUGGING_PORT': None 远程调试端口：未设置（无远程调试端口）
    # 'IGNORE_SSL_ERRORS': False 忽略SSL错误：关闭（不忽略SSL错误）
    webview.settings['IGNORE_SSL_ERRORS'] = True  # 忽略SSL错误：关闭（不忽略SSL错误）
    webview.settings['OPEN_EXTERNAL_LINKS_IN_BROWSER'] = True  # 在浏览器中打开外部链接：（True外部链接将在浏览器中打开）
    webview.settings['OPEN_DEVTOOLS_IN_DEBUG'] = False  # 调试时打开开发者工具：关闭（在调试模式下自动打开开发者工具）
    webview.settings['ALLOW_DOWNLOADS'] = True  # 是否允许下载：关闭（不允许下载）
    # ------窗口绑定(使用才绑定,过渡绑定对低配置电脑卡)--------
    api.windows[0].events.closed += api.on_closed  # 窗口事件,窗口关闭事件
    api.windows[0].events.closing += api.on_closing  # 窗口事件,窗口关闭事件
    api.windows[0].events.shown += api.on_shown  # 窗口事件,窗口显示事件
    # api.windows[0].events.loaded += api.on_loaded  # 窗口事件,窗口加载事件
    # api.windows[0].events.minimized += api.on_minimized  # 窗口事件,窗口最小化事件
    # api.windows[0].events.maximized += api.on_maximized  # 窗口事件,窗口最大化事件
    # api.windows[0].events.restored += api.on_restored  # 窗口事件,窗口还原事件
    # api.windows[0].events.resized += api.on_resized  # 窗口事件,窗口大小改变事件
    # api.windows[0].events.moved += api.on_moved  # 窗口事件,窗口位置改变事件
    # api.windows[0].expose(lol, wtf) # 将函数暴露给 Javascript
    # ------启动参数--------
    # 配置pywebview关闭提示的中文翻译
    chinese_localization = {
        'global.quitConfirmation': '确定要关闭吗？',

    }
    http_port = api.get_random_unused_port()
    api.log("info", f'指定端口号{http_port}')
    if not http_port:
        return False
    # 启动webview
    webview.start(
        debug=False,  # 是否启动调试模式,打开控制台
        http_port=http_port,  # 指定端口号
        func=api.StartTask,  # 启动额外线程,执行任务
        localization=chinese_localization,  # 设置中文本地化
    )
