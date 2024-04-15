from .database import Base
from sqlalchemy import Column, Integer, String, JSON

class JobPost(Base):
    __tablename__ = 'job_posts'

    id = Column(Integer, primary_key=True)
    main_field = Column(String, index=True)  # 주요분야
    num_posts = Column(Integer)              # 관련된 채용공고의 수
    related_field = Column(JSON)             # 관련된 기술 필드 및 그 카운트를 저장하는 JSON 필드

    def __repr__(self):
        return f"<JobPost(id={self.id}, main_field='{self.main_field}', num_posts={self.num_posts})>"
