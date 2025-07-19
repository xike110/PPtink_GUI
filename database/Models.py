"""
数据库模型文件
使用SQLite数据库 + SQLAlchemy ORM
"""
import os
import datetime
import contextlib
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, Table, JSON
from sqlalchemy.orm import relationship, sessionmaker, declarative_base

# 数据库连接
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database.db')
# 2. 创建引擎
engine = create_engine(
    f"sqlite:///{DB_PATH}",
    connect_args={"check_same_thread": False},  # 仅SQLite需要，允许多线程访问
    echo=False,  # 显示SQL语句
    # pool_size=5,  # 连接池大小
    # max_overflow=10,  # 最大溢出连接数
    # pool_timeout=30,  # 获取连接超时时间(秒)
    # pool_recycle=3600  # 连接回收时间(秒)
)

# 创建会话
Session = sessionmaker(
    bind=engine,  # 创建会话
    # autocommit=False,  # 关闭自动提交
    # autoflush=False,  # 关闭自动刷新
)
session = Session()

# 创建基类
Base = declarative_base()


# 会话管理上下文，自动处理提交、回滚和关闭
@contextlib.contextmanager
def session_scope():
    """提供事务范围的会话对象。
    自动处理提交或回滚事务并关闭会话。
    使用方式:
    with session_scope() as session:
        session.add(some_object)
        session.add(some_other_object)
    """
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"数据库操作出错，已回滚: {str(e)}")
        raise
    finally:
        session.close()


class App(Base):
    __tablename__ = 'apps'

    id = Column(Integer, primary_key=True, autoincrement=True, comment='应用ID主键')
    name = Column(String(100), nullable=False, comment='应用名称')
    belongs = Column(Boolean, default=False, comment='应用归属')  # True=系统归属 False=客户添加
    category = Column(String(50), nullable=False, comment='应用分类')
    description = Column(Text, nullable=True, comment='应用描述')
    icon = Column(String(255), nullable=True, comment='应用图标路径')
    bgcolor = Column(String(50), default='#e6f7ff', comment='应用背景颜色')
    type = Column(String(50), nullable=False, comment='应用类型')  # 应用类型 builtin = 应用软件, external = 外部软件 link = 链接
    open = Column(String(1024), nullable=False, comment='打开命令或路径')  # 应用软件路径="WebMain.main_str" 外部软件路径="C:\Windows\System32\calc.exe" 链接="https://www.pptink.com"
    recommend = Column(Boolean, default=False, comment='是否推荐')
    isview = Column(Boolean, default=True, comment='是否可见')
    created_at = Column(DateTime, default=datetime.datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now, comment='更新时间')


# 创建所有表
def init_db():
    Base.metadata.create_all(engine)  # 创建所有表


if __name__ == "__main__":
    init_db()
