import logging
import time
import asyncio  # 导入 asyncio 库
import json
import os
import stat
import sys
from app.WebDemo.utils import conf
import webview
from app.WebDemo.common.validate import Verify


class Task(Verify):
    def __init__(self):
        """
        初始化Task对象
        参数:
        返回:
            无
        """
        super().__init__()  # 调用父类构造函数

    def process_args(self, args):
        """
        解析参数执行具体任务
        :param args: 参数字典
        :return:
        """
        if not args:
            self.runlog("未接收到参数，使用默认值", "warning")
            return

        # 记录参数值到日志
        for key, value in args.items():
            self.runlog(f"参数 {key}: {value}", "info")
        total_steps = 100
        for step in range(1, total_steps + 1):
            # if stop_event.is_set():
            #  return
            time.sleep(0.1)
            progress = int((step / total_steps) * 100)
            js_progress = f"window.logStore.progressPercentage.value = {progress}"
            self.windows[0].evaluate_js(js_progress)
            self.runlog(f"进度: {progress}%", "info")
            time.sleep(0.1)


if __name__ == "__main__":
    pass
