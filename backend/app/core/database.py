import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 确保database目录存在
database_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../database"))
os.makedirs(database_dir, exist_ok=True)

# 数据库URL
DATABASE_URL = f"sqlite:///{os.path.join(database_dir, 'homework.db')}"

# 创建SQLAlchemy引擎
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# 创建会话类
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建Base类
Base = declarative_base()


# 依赖项，用于获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()