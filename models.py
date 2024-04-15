# DB의 데이터 테이블을 정의한다.

from sqlalchemy import Column, Integer, String, DateTime, JSON

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

class Wanted(Base):
    __tablename__ = "wanted"

    id = Column(Integer, primary_key=True)
    company = Column(String, nullable=False)
    title = Column(String, nullable=False)
    options = Column(String, nullable=False)
    techs = Column(String, nullable=False)
    link = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False)

class JobPost(Base):
    __tablename__ = 'job_posts'

    id = Column(Integer, primary_key=True)
    main_field = Column(String, nullable=False)
    num_posts = Column(Integer, nullable=False)
    related_field = Column(JSON, nullable=True) # 데이터 타입을 일정하게 설정해야됨