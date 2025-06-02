import datetime
import logging
import os
import yaml
from diskcache import Cache  # 缓存

# ======================= 软件窗口配置 ==========================
DEBUG = True  # 开启DEBUG
BRANDNAME = "PPtink"  # 品牌名
SIGN = "WebDemo"  # 软件标识-自动生成勿修改
GUI_NAME = f"PPtink桌面免费版"  # GUI名称
GUI_VERSION = "1.0.2"  # GUI版本
GUI_DATE = "2025-03-23"  # 最新版发布日期
GUI_INTRODUCE = "生命不止,奋斗不息!"  # 不超过10个字的广告语
GUI_DESCRIPTION = F"{GUI_NAME}，致力于为用户提供简洁、高效、现代化的桌面应用开发体验。我们采用最新的技术栈和设计理念，确保为开发者提供最佳的开发体验和工具支持。"  # 软件介绍-128字以内
ICO_LOGO = "./ico/logo.png"  # 软件图标
GUI_THEME = "light"  # 启动默认主题 light=白色主题,dark=黑色主题
GUI_COLORS = "#CCCCFF"  # 主题副颜色 #CCCCFF=紫色主题 #99CCFF=蓝色主题 #99CCCC=绿色主题 #EEEEEE=灰色主题
GUI_POWER = (1024, 1024)  # 分辨率
GUI_FULLSCREEN = True  # 是否允许最大化全屏
GUI_FULLSCREENSTARTUP = False  # True=使用全屏启动  False=使用上面自定义尺寸
PERSON = "微信:xikejian"  # 联系方式
OPENLOGIN = False  # 是否开启登录窗口
IS_NETWORK = True  # 是否检查网络,用户网络状态不通时，GUI拒绝启动，提示用户网络故障,检查网络！
GUI_PORT = 55697  # 软件端口
REPEATEDSTARTUP = False  # 设置True后允许一个应用添加多个开机启动和定时任务,默认False防止某些单线程任务重复执行造成错误，如果你确定任务可以重复执行可以设置为True
HEADER = True  # 是否使用自定义头部，True=开启 False=关闭使用系统头
# ======================= 业务配置 ==========================
DOMAINNAME = "https://www.pptink.com"  # 服务域名
cache = Cache(F"cache")  # 初始化缓存目录
with open('./config/config.yaml', 'r', encoding='utf-8') as file:
    yaml_data = yaml.load(file, Loader=yaml.FullLoader)  # 加载外部YAML文件
DIST_DIR = F"{os.getcwd()}/vuecode/dist/webdemo.html"  # 软件主界面的WEB路径="webdemo.html"
# ======================= 组件配置 ==========================
# redis_cache = redis.Redis(host='121.11.119.111', port=36379, db=10, password='123456')
# ======================= 日志配置 ==========================
# 日志配置-日志文件大小50MB 保留10份,在原日志文件追加
LOG_MAX_BYTES = 50 * 1024 * 1024  # 日志文件大小
LOG_MAX_SIZE = 50 * 1024 * 1024  # 日志文件大小
LOG_DIR = "log"
LOG_BACKUP_COUNT = 10
LOG_FILENAME = F"log/log_{datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')}.log"  # 日志文件路径
LOG_LEVEL = logging.DEBUG
logging.basicConfig(
    filename=LOG_FILENAME,
    level=LOG_LEVEL,
    format='%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filemode='w',
    encoding='utf-8'

)
# ======================= 内容配置 ==========================
ASKED_QUESTIONS = [
    {
        "question": "如何报告Bug或提出建议？",
        "answer": "您可以通过\"帮助\"菜单中的\"反馈\"功能向我们报告问题或提出建议。也可以直接发送邮件至我们的支持邮箱，我们会尽快回复并处理您的反馈。"
    },
    {
        "question": "软件更新频率是多久？",
        "answer": "我们通常每月发布一次功能更新，每周发布一次小型修复更新。您可以在\"设置\"中选择自动更新选项，以确保总是使用最新版本。"
    },
    {
        "question": "如何提高软件运行速度？",
        "answer": "您可以尝试清理缓存（在\"设置\"→\"性能优化\"中），关闭不必要的后台进程，定期重启应用，以及确保您的设备符合推荐的系统要求。"
    }
]
ABOUTUS = F"""
<div class="about-content">
<div class="about-item">
<h3>软件介绍</h3>
<p>{GUI_NAME}，致力于为用户提供简洁、高效、现代化的桌面应用开发体验。我们采用最新的技术栈和设计理念，确保为开发者提供最佳的开发体验和工具支持。</p>
</div>

<div class="about-item">
<h3>核心特性</h3>
<ul>
<li>现代化界面设计，支持明暗主题切换</li>
<li>完整的组件库，快速构建专业应用</li>
<li>灵活的配置系统，满足个性化需求</li>
<li>强大的扩展性，支持插件开发</li>
<li>跨平台支持，一次开发多端运行</li>
</ul>
</div>

<div class="about-item">
<h3>技术支持</h3>
<p>我们提供专业的技术支持服务，确保您的开发过程顺利进行：</p>
<ul>
<li>📧 邮箱：support@pptink.com</li>
<li>💬 官方论坛：forum.pptink.com</li>
<li>📱 微信公众号：PPtink </li>
<li>✔️ 微信：{PERSON}</li>
</ul>
</div>

<div class="about-item">
<h3>版本信息</h3>
<p>最新版本：{GUI_VERSION}</p>
<p>发布日期：{GUI_DATE}</p>
<p>版权所有 © 2025 PPtink Team. 保留所有权利。</p>
</div>

<div class="about-item">
<h3>加入我们</h3>
<p>我们始终欢迎优秀的开发者加入我们的团队。如果您对桌面应用开发充满热情，欢迎通过以下方式联系我们：</p>
<ul>
<li>📮 招聘邮箱：hr@pptink.com</li>
<li>🌐 官方网站：<a href="https://gui.pengxukeji.cn" target="_blank">https://gui.pengxukeji.cn</a></li>
</ul>
</div>
</div>
"""
