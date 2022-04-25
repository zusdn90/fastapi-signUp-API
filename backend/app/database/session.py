from sqlalchemy import create_engine, engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager

SQLALCHEMY_DATABASE_URI = "sqlite:///./sql_app.db"
print(f"db connection url : {SQLALCHEMY_DATABASE_URI}")

engine = create_engine(
    SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}
)
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
