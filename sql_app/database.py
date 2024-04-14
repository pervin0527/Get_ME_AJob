from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# "postgresql://postgres:비밀번호@localhost/db명"
SQLALCHEMY_DATABASE_URL = "postgresql://postgre:wldnjs5768@@localhost/test_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()