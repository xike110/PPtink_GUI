import logging
import time
import asyncio  # 导入 asyncio 库
import json
import os
import stat
import sys
import webview
import socket  # 导入socket模块用于端口检测


class Server:
    def __init__(self, port="8080", host='0.0.0.0', dict_data=None, RunCode=None):
        """
        初始化Task对象
        参数:
        返回:
            无
        """
        self.port = port
        self.host = host
        self.dict_data = dict_data
        self.RunCode = RunCode

    def __setattr__(self, key, value):
        """
        对象属性设置时的约束检查
        参数:
            key (str): 属性名
            value: 属性值
        返回:
            无
        """
        # self.runlog(f'参数检查名:{key}参数检查值:{value}')
        return object.__setattr__(self, key, value)

    def check_port_in_use(self, port, host='127.0.0.1'):
        """
        检查端口是否被占用
        :param port: 端口号
        :param host: 主机地址
        :return: 如果端口被占用返回True，否则返回False
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind((host, int(port)))
            return False
        except socket.error:
            return True
        finally:
            s.close()

    def run(self, dict_data=None):
        """
        启动WEB服务
        :param dict_data: 前端传来的参数字典
        :return: None
        """
        try:
            # 检查端口是否被占用
            if self.check_port_in_use(self.port):
                self.RunCode.runlog(f"警告：端口 {self.port} 已被占用，服务可能无法正常启动", "warning")
                return {"status": "error", "message": f"端口 {self.port} 已被占用，服务无法启动"}

            # 导入FastAPI相关库
            from fastapi import FastAPI, Request, HTTPException
            from fastapi.middleware.cors import CORSMiddleware
            from fastapi.responses import JSONResponse
            from fastapi.staticfiles import StaticFiles
            from fastapi.openapi.docs import get_swagger_ui_html
            import uvicorn
            import threading
            import os

            # 在这里导入conf模块，避免循环导入
            # from app.WebDemo.utils import conf

            # 创建FastAPI应用
            app = FastAPI(
                title=f"API服务",
                description="FastAPI服务接口",
                version="1.0.0",
                docs_url=None  # 禁用默认的文档页面，我们将使用自定义文档页面
            )

            # 添加CORS中间件
            app.add_middleware(
                CORSMiddleware,
                allow_origins=["*"],  # 允许所有来源
                allow_credentials=True,
                allow_methods=["*"],  # 允许所有方法
                allow_headers=["*"],  # 允许所有头
            )

            # 挂载静态文件目录
            static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static")
            app.mount("/static", StaticFiles(directory=static_dir), name="static")

            # 全局异常处理
            @app.exception_handler(Exception)
            async def global_exception_handler(request: Request, exc: Exception):
                logging.error(f"全局异常: {exc}")
                return JSONResponse(
                    status_code=500,
                    content={"message": "服务器内部错误", "detail": str(exc)}
                )

            # 根路由
            @app.get("/")
            async def root():
                return {"message": "欢迎使用API服务", "version": "1.0.0"}

            # 健康检查路由
            @app.get("/health")
            async def health_check():
                return {"status": "ok", "timestamp": time.time()}

            # 如果有传入参数，添加一个API路由来获取这些参数
            if dict_data:
                @app.get("/params")
                async def get_params():
                    return dict_data

            # 添加自定义Swagger UI文档路由
            @app.get("/docs", include_in_schema=False)
            async def custom_swagger_ui():
                return get_swagger_ui_html(
                    openapi_url="/openapi.json",
                    title="API服务 - Swagger UI",
                    swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
                    swagger_css_url="/static/swagger-ui/swagger-ui.css",
                    swagger_favicon_url="/static/swagger-ui/favicon.png"
                )

            local_ip = socket.gethostbyname(socket.gethostname())  # 获取本地IP地址
            self.RunCode.runlog(f"外部访问地址: http://{local_ip}:{self.port}", "info")
            self.RunCode.runlog(f"本地访问地址 http://127.0.0.1:{self.port}", "info")
            self.RunCode.runlog(f"API文档地址: http://127.0.0.1:{self.port}/docs", "info")
            self.RunCode.runlog(f"可以关闭本窗口,服务在后台运行,关闭主程序,服务停止运行", "debug")

            # 在单独的线程中启动服务，避免阻塞主线程
            def start_server():
                try:
                    uvicorn.run(app, host=self.host, port=int(self.port), log_level="info")
                except Exception as e:
                    logging.error(f"启动FastAPI服务失败: {e}")

            # 创建并启动服务线程
            server_thread = threading.Thread(target=start_server, daemon=True)
            server_thread.start()

            return {"status": "success", "message": f"FastAPI服务已在 http://127.0.0.1:{self.port} 启动"}

        except Exception as e:
            logging.error(f"启动WEB服务失败: {e}")
            return {"status": "error", "message": f"启动服务失败: {str(e)}"}
