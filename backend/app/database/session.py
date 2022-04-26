from sqlalchemy import create_engine, engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from app.core.common.config import settings


print(f"db connection url : {settings.SQLALCHEMY_DATABASE_URI}")

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True, echo=False
)  # pool_pre_ping -> select 1 같은 간단한 쿼리문으로 connection 확인
db_session = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_db():
    db = db_session()
    try:
        yield db
        db.commit()
    except:
        print("db rollback...")
        db.rollback()
        raise
    finally:
        print("close Database")
        db.close()
