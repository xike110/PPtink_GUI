import tkinter as tk
from tkinter import messagebox
import sys
import threading
import time


def show_popup(tiele: str = "发生错误!", message: str = "输入有误"):
    """弹窗"""
    # 使用messagebox模块来显示弹窗
    result = messagebox.askokcancel(
        tiele,  # 弹窗的标题
        message  # 弹窗的消息内容
    )
    # askokcancel会返回一个布尔值，True表示用户点击了"确定"，False表示点击了"取消"
    if result:
        print("用户点击了确定")
        return True
    else:
        print("用户点击了取消")
        return False

