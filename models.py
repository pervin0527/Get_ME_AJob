# DB의 데이터 테이블을 정의한다.

from sqlalchemy import Column, Integer, String, Text, DateTime

from database import Base

class Jobkorea(Base):
    __tablename__ = "jobkorea"

    id = Column(Integer, primary_key=True)
    company = Column(String, nullable=False)
    title = Column(String, nullable=False)
    options = Column(String, nullable=False)
    techs = Column(String, nullable=False)
    link = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False)

class Saramin(Base):
    __tablename__ = "saramin"

    id = Column(Integer, primary_key=True)
    company = Column(String, nullable=False)
    title = Column(String, nullable=False)
    options = Column(String, nullable=False)
    techs = Column(String, nullable=False)
    link = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False)

class FieldAnal(Base):
    __tablename__ = 'field_anal'

    id = Column(Integer, primary_key=True)
    field = Column(String, nullable=False)
    count = Column(Integer, nullable=False)