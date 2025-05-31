from fastapi.openapi.docs import get_swagger_ui_html
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

def custom_swagger_ui_html():
    """
    生成自定义的Swagger UI HTML，使用本地资源而不是CDN
    """
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="API服务 - Swagger UI",
        swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui/swagger-ui.css",
        swagger_favicon_url="/static/swagger-ui/favicon.png"
    )

def setup_static_files(app: FastAPI):
    """
    配置静态文件服务
    """
    app.mount("/static", StaticFiles(directory="app/WebDemo/static"), name="static")

def setup_custom_docs(app: FastAPI):
    """
    配置自定义文档页面
    """
    # 禁用默认的文档
    app.docs_url = None
    
    # 添加自定义文档路由
    @app.get("/docs", include_in_schema=False)
    async def custom_docs():
        return custom_swagger_ui_html()