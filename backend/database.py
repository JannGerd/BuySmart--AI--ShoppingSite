from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:Buysmart123@localhost/buysmart"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()