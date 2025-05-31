import os
# import sys
import sys
# import signal
# import datetime
import argparse
import logging
import psutil

from app.WebDemo import WebMain
from utils import Request
from app.WebDemo.utils import conf
from utils import gui_tkinter
from database import Models
import os.path


# 打印当前程序运行目录
# logging.info(F"当前程序运行目录:{os.getcwd()}")
def main_init(autostart=1):
    """
    autostart 0为开机自动启动，1为用户手动启动
    """
    # 检查数据库是否已初始化
    check_and_init_database()

    # 正常显示主窗口
    if conf.OPENLOGIN:
        "开启了登录"
        if conf.IS_NETWORK:
            sh_init = Request.Task(None, None, conf.DOMAINNAME)
            if not sh_init.aivideo_ceshi():
                gui_tkinter.show_popup("网络错误！", F"你的网络不稳定或者不正常！程序无法启动！请先解决你的网络问题！")
                sys.exit()
        is_uid = conf.cache.get('uid', None)
        is_token = conf.cache.get('token', None)
        logging.info(F"{is_uid}{is_token}")
        if is_uid and is_token:
            "已经登录,直接启动界面"
            WebMain.main_init(autostart=autostart)
        else:
            "未登录,启动登录界面"
            # todo 登录界面 未完成编写
            WebMain.main_init(autostart=autostart)
    else:
        if conf.IS_NETWORK:
            sh_init = Request.Task(None, None, conf.DOMAINNAME)
            if not sh_init.aivideo_ceshi():
                gui_tkinter.show_popup("网络错误！", F"你的网络不稳定或者不正常！程序无法启动！请先解决你的网络问题！")
                sys.exit()
        WebMain.main_init(autostart=autostart)


def check_already_running():
    """
    检测是否已经有相同程序在运行
    :return: True表示已有程序在运行，False表示没有
    """
    current_process = psutil.Process(os.getpid())
    current_process_name = current_process.name()

    for process in psutil.process_iter(['pid', 'name']):
        # 跳过当前进程
        if process.info['pid'] == current_process.pid:
            continue
        # logging.info(F"{current_process_name}")
        # 检查是否有同名进程
        if process.info['name'] == current_process_name and current_process_name != "python.exe":
            return True

    return False


def check_and_init_database():
    """
    检查数据库是否已初始化，如果没有则初始化数据库
    """
    db_path = Models.DB_PATH
    db_dir = os.path.dirname(db_path)

    # 确保数据库目录存在
    if not os.path.exists(db_dir):
        try:
            os.makedirs(db_dir)
            logging.info(f"创建数据库目录: {db_dir}")
        except Exception as e:
            logging.error(f"创建数据库目录失败: {str(e)}")
            gui_tkinter.show_popup("数据库错误", f"创建数据库目录失败: {str(e)}\n程序无法正常启动！")
            sys.exit(1)

    # 检查数据库文件是否存在
    if not os.path.exists(db_path):
        logging.info("数据库文件不存在，正在初始化...")
        try:
            Models.init_db()
            logging.info("数据库初始化成功")
        except Exception as e:
            logging.error(f"数据库初始化失败: {str(e)}")
            gui_tkinter.show_popup("数据库错误", f"数据库初始化失败: {str(e)}\n程序无法正常启动！")
            sys.exit(1)


if __name__ == '__main__':
    # 检测是否已经有相同程序在运行
    if check_already_running():
        gui_tkinter.show_popup("程序已在运行", "程序已经在运行，请勿重复启动！\n查看左下角最小化图标")
        sys.exit()

    parser = argparse.ArgumentParser()
    parser.add_argument('--autostart', action='store_true', help='标识是否为开机自动启动')
    args = parser.parse_args()
    if args.autostart:
        logging.info("开机自动启动")
        # print("这是开机自动启动")
        main_init(0)
    # 执行开机启动特有的逻辑，如最小化到托盘
    else:
        # logging.info("用户主动启动")
        # print("这是用户主动启动")
        main_init(1)
