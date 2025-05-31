import logging
import json
import os
import stat
import sys
import webview
import ctypes
from app.WebDemo.utils.WebHome import Home
from app.WebDemo.utils import conf
import asyncio  # 导入 asyncio 库
import time
import threading
import queue
from database import Models


class Function(Home):
    """
    交互功能函数
    """

    def __init__(self):
        super().__init__()  # 调用父类构造函数

    def get_config(self):
        """
        获取配置信息
        """
        return {
            'GUI_NAME': conf.GUI_NAME,  # 窗口名称
            'SIGN': conf.SIGN,  # 标识
            'MAIN': self.main,  # 入口地址
            'RUNPARAMS': self.formdata,  # 开机启动表单数据
            'GUI_VERSION': conf.GUI_VERSION,  # 窗口版本
            'GUI_INTRODUCE': conf.GUI_INTRODUCE,  # 窗口介绍
            'GUI_COLORS': conf.GUI_COLORS,  # 主题颜色
            'PERSON': conf.PERSON,  # 联系方式
            'DOMAINNAME': conf.DOMAINNAME,  # 域名
            'BRANDNAME': conf.BRANDNAME,  # 品牌名
            'GUI_FULLSCREEN': conf.GUI_FULLSCREEN,  # 是否允许最大化全屏
            'GUI_THEME': conf.GUI_THEME,  # 主题颜色
            'ICO_LOGO': conf.ICO_LOGO,  # ico 图标
            'ASKED_QUESTIONS': conf.ASKED_QUESTIONS,  # 常见问题
            'ABOUTUS': conf.ABOUTUS,  # 关于我们
        }

    def StartTask(self):
        """
        启动额外线程,执行程序,启动托盘图表菜单
        """
        # 启动软件执行
        logging.info('子窗口应用检测环境')
        logging.info('子窗口应用检测环境完毕')

    def runlog(self, value=None, tpre_str="info", ):
        """
        运行日志 同时回调前端JS 函数实现运行日志本地与前端双输出
        """
        # 判定 value类型是否为字典
        if isinstance(value, dict):
            value = json.dumps(value, indent=2, ensure_ascii=False)
        if tpre_str == "info":
            logging.info(F"{self.sign}:{value}")
        elif tpre_str == "error":
            logging.error(F"{self.sign}:{value}")
        elif tpre_str == "warning":
            logging.warning(F"{self.sign}:{value}")
        elif tpre_str == "debug":
            logging.debug(F"{self.sign}:{value}")
        elif tpre_str == "critical":
            logging.critical(F"{self.sign}:{value}")
        else:
            logging.info(F"{self.sign}:{value}")

        # 将日志发送到前端
        try:
            if self.windows and len(self.windows) > 0:
                # 构造JavaScript代码，调用前端的logStore.addLog函数
                js_code = f"window.logStore.addLog({json.dumps(value)}, {json.dumps(tpre_str)})"
                self.windows[0].evaluate_js(js_code)
                return True
            return False
        except Exception as e:
            logging.error(f"向前端发送日志失败: {e}")
            return False

    def _monitor_runstate(self, task_queue):
        """
        监控runstate状态的线程函数
        """
        while True:
            if not self.runstate:
                # 发送终止信号到程序队列
                task_queue.put(True)
                break
            time.sleep(0.5)  # 每500毫秒检查一次状态

    def get_gui_config(self):
        """
        获取GUI配置信息，供前端动态生成菜单和表单
        :return: GUI配置信息
        """
        try:
            from app.WebDemo.RunCode import RunCode
            runcode = RunCode()
            return runcode.get_menu_config()
        except Exception as e:
            logging.error(f"获取GUI配置失败: {str(e)}")
            return {"error": str(e)}

    def RunArgs(self, params=None):  # 修改参数接收方式
        """
        界面回调运行参数
        """
        dict_data = params if params else {}
        logging.info(f'运行参数:{dict_data}')

        # 检查是否收到参数
        if not dict_data:
            self.runlog("未收到有效参数", "error")
            return {"success": False, "message": "未收到有效参数"}

        try:
            # 设置运行状态为true
            self.runstate = True

            # 创建线程间通信的队列
            task_queue = queue.Queue()  # 用于向程序线程发送终止信号
            result_queue = queue.Queue()  # 用于获取程序线程的执行结果

            # 创建执行RunMain的线程
            execute_thread = threading.Thread(
                target=self._execute_runmain,
                args=(dict_data, task_queue, result_queue),
                daemon=True  # 设置为守护线程，主线程结束时自动结束
            )

            # 创建监控线程
            monitor_thread = threading.Thread(
                target=self._monitor_runstate,
                args=(task_queue,),
                daemon=True  # 设置为守护线程，主线程结束时自动结束
            )

            # 启动线程
            execute_thread.start()
            monitor_thread.start()

            # 等待执行线程完成并获取结果
            execute_thread.join()
            return result_queue.get()

        except Exception as e:
            # 发生错误时，设置进度条状态为异常
            js_status = "window.logStore.progressStatus.value = 'exception'"
            self.windows[0].evaluate_js(js_status)
            self.runlog(f"程序执行失败: {str(e)}", "error")
            return {"success": False, "message": str(e)}

        finally:
            # 无论成功还是失败，都将运行状态设置为false
            if not self.formdata:
                self.runstate = False
            if self.father_data.get("autoclose"):
                # 判断是否自动关闭窗口
                time.sleep(3)
                self.destroy()  # 关闭窗口
            return None

    def _execute_runmain(self, dict_data, task_queue, result_queue):
        """
        执行RunMain函数的线程函数，可以被外部中断
        """
        try:
            # 设置一个事件对象用来通知线程退出
            exit_event = threading.Event()

            # 创建一个监控子线程，用于检查退出事件
            def check_exit():
                while not exit_event.is_set():
                    try:
                        terminate = task_queue.get_nowait()
                        if terminate:
                            # 如果收到终止信号，设置退出事件
                            exit_event.set()
                            # 发送信息到结果队列
                            result_queue.put({"success": False, "message": "程序被用户中止"})
                            self.runlog("程序中止", "warning")
                            # 获取当前线程上下文的主线程，如果已经退出则中断
                            for thread in threading.enumerate():
                                if thread.name == f"{self.sign}_task" and thread.is_alive():
                                    try:
                                        raise_exception_in_thread = ctypes.pythonapi.PyThreadState_SetAsyncExc
                                        thread_id = ctypes.c_long(thread.ident)
                                        exception = ctypes.py_object(SystemExit)
                                        raise_exception_in_thread(thread_id, exception)
                                    except Exception as e:
                                        self.runlog(f"中断{self.sign}线程失败: {str(e)}", "error")
                                    return
                    except queue.Empty:
                        pass
                    time.sleep(0.5)  # 每500毫秒检查一次状态

            # 启动监控子线程
            monitor_subthread = threading.Thread(target=check_exit, daemon=True)
            monitor_subthread.start()

            # 创建一个线程来执行RunMain函数
            main_thread = threading.Thread(
                target=self.RunMain,
                args=(dict_data,),
                daemon=True,
                name=f"{self.sign}_task"  # 给线程一个特定名称便于识别
            )
            js_progress = "window.logStore.progressPercentage.value = 1"  # 设置进度条为1
            self.windows[0].evaluate_js(js_progress)  # 设置进度条为1
            main_thread.start()

            # 等待主线程完成或被中断
            while main_thread.is_alive() and not exit_event.is_set():
                main_thread.join(0.5)  # 每0.5秒检查一次线程状态

            # 如果是正常完成（而不是被中断），发送成功消息
            if not exit_event.is_set():
                if not self.formdata:
                    self.runstate = False
                result_queue.put({"success": True, "message": "程序执行完成"})
                js_progress = "window.logStore.progressPercentage.value = 100"
                self.windows[0].evaluate_js(js_progress)
                js_status = "window.logStore.progressStatus.value = 'success'"
                self.windows[0].evaluate_js(js_status)
                self.runlog("程序执行完成！", "info")

        except Exception as e:
            if not self.formdata:
                self.runstate = False
            # 发生错误时，设置进度条状态为异常
            js_status = "window.logStore.progressStatus.value = 'exception'"
            self.windows[0].evaluate_js(js_status)
            self.runlog(f"{self.sign}执行失败: {str(e)}", "error")
            result_queue.put({"success": False, "message": str(e)})

    def SaveParamsToStartup(self, params):
        """
        保存参数到开机启动数据库
        :param params: 要保存的参数，应包含gui_name(窗口名称), sign(标识), menuName(菜单名称), formData(表单数据)
        :return: 保存结果
        """
        try:
            # 检查参数是否有效
            if not params:
                self.runlog("未收到有效的开机启动参数", "error")
                return {"success": False, "message": "未收到有效参数"}

            # 提取参数
            guiname = params.get('gui_name', '')
            sign = params.get('sign', '')
            main = params.get('main', '')
            menuname = params.get('menuName', '')
            formdata = params

            if not guiname or not sign or not menuname:
                self.runlog(f"保存开机启动参数缺少必要参数: {params}", "error")
                return {"success": False, "message": "缺少必要参数"}

            # 记录日志
            self.runlog(f"正在保存开机启动参数: {json.dumps(params, ensure_ascii=False)}", "info")

            # 使用事务保存到数据库
            with Models.session_scope() as session:
                # 只检查sign字段是否有重复记录
                exist_record = session.query(Models.StartupApp).filter(
                    Models.StartupApp.sign == sign
                ).first()

                if exist_record and not conf.REPEATEDSTARTUP:
                    # 如果存在则更新记录
                    exist_record.guiname = guiname
                    exist_record.main = main
                    exist_record.menuname = menuname
                    exist_record.formdata = formdata
                    exist_record.enabled = True
                    exist_record.bkgrdstat = False
                    exist_record.autoclose = False
                    exist_record.priority = 0
                    exist_record.delay = 3
                    self.runlog(f"更新已存在的开机启动记录(sign={sign}): {guiname}/{menuname}", "info")
                else:
                    # 如果不存在则创建新记录
                    new_startup = Models.StartupApp(
                        guiname=guiname,
                        sign=sign,
                        main=main,
                        menuname=menuname,
                        formdata=formdata,
                        enabled=True,
                        bkgrdstat=False,
                        autoclose=False,
                        priority=0,
                        delay=3
                    )
                    session.add(new_startup)
                    self.runlog(f"创建新的开机启动记录(sign={sign}): {guiname}/{menuname}", "info")

            return {"success": True, "message": "保存到开机启动成功"}
        except Exception as e:
            self.runlog(f"保存开机启动参数出错: {str(e)}", "error")
            return {"success": False, "message": str(e)}

    def SaveParamsToTimed(self, params):
        """
        保存参数到定时任务数据库
        :param params: 要保存的参数，应包含gui_name(窗口名称), sign(标识), menuName(菜单名称), formData(表单数据)
        :return: 保存结果
        """
        try:
            # 检查参数是否有效
            if not params:
                self.runlog("未收到有效的定时任务参数", "error")
                return {"success": False, "message": "未收到有效参数"}

            # 提取参数
            guiname = params.get('gui_name', '')
            sign = params.get('sign', '')
            main = params.get('main', '')
            menuname = params.get('menuName', '')
            formdata = params

            if not guiname or not sign or not menuname:
                self.runlog(f"保存定时任务参数缺少必要参数: {params}", "error")
                return {"success": False, "message": "缺少必要参数"}

            # 记录日志
            self.runlog(f"正在保存定时任务参数: {json.dumps(params, ensure_ascii=False)}", "info")

            # 使用事务保存到数据库
            with Models.session_scope() as session:
                # 只检查sign字段是否有重复记录
                exist_record = session.query(Models.TimedApp).filter(
                    Models.TimedApp.sign == sign
                ).first()

                if exist_record:
                    # 如果存在则更新记录
                    exist_record.guiname = guiname
                    exist_record.main = main
                    exist_record.menuname = menuname
                    exist_record.formdata = formdata
                    exist_record.timedtype = None  # 默认定时类型为分钟
                    exist_record.timedvalue = None  # 默认定时值为30
                    exist_record.enabled = True
                    exist_record.bkgrdstat = False
                    exist_record.autoclose = True
                    self.runlog(f"更新已存在的定时任务记录(sign={sign}): {guiname}/{menuname}", "info")
                else:
                    # 如果不存在则创建新记录
                    new_timed = Models.TimedApp(
                        guiname=guiname,
                        sign=sign,
                        main=main,
                        menuname=menuname,
                        formdata=formdata,
                        timedtype=None,  # 默认定时类型为分钟
                        timedvalue=None,  # 默认定时值为30
                        enabled=True,
                        bkgrdstat=False,
                        autoclose=True
                    )
                    session.add(new_timed)
                    self.runlog(f"创建新的定时任务记录(sign={sign}): {guiname}/{menuname}", "info")

            return {"success": True, "message": "保存到定时任务成功"}
        except Exception as e:
            self.runlog(f"保存定时任务参数出错: {str(e)}", "error")
            return {"success": False, "message": str(e)}
