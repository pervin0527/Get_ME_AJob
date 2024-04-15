# crud를 통해 DB에서 데이터를 가져올 때 적절한 형식을 맞춰서 가져오는지 검사할 때 사용
# 미리 데이터들의 형태를 정의해둔다.

import datetime

import json
from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any


class Jobkorea(BaseModel):
    id: int
    company: str
    title: str
    options: str
    techs: str
    link: str
    create_date: datetime.datetime

    class Config:
        orm_mode = True

class Saramin(BaseModel):
    id: int
    company: str
    title: str
    options: str
    techs: str
    link: str
    create_date: datetime.datetime

    class Config:
        orm_mode = True

class Detail(BaseModel):
    id: int
    company: str
    title: str
    options: str
    techs: str
    link: str
    create_date: datetime.datetime

    class Config:
        orm_mode = True

class JobPostBase(BaseModel):
    id: int
    main_field: str
    num_posts: int
    related_field: Optional[List[Dict[str, Any]]] = None # 데이터 타입을 일정하게 설정해야됨

    @validator('related_field', pre=True, always=True)
    def ensure_json(cls, v):
        if isinstance(v, str):
            v = v.replace("'", '"')  # 작은따옴표를 큰따옴표로 변환
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("related_field must be a valid JSON list")
        return v

    class Config:
        orm_mode = True