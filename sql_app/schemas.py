import json

from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator

class JobPostBase(BaseModel):
    main_field: str
    num_posts: int
    related_field: Optional[List[Dict[str, Any]]] = None

    @validator('related_field', pre=True, always=True)
    def ensure_json(cls, v):
        if isinstance(v, str):
            v = v.replace("'", '"')  # 작은따옴표를 큰따옴표로 변환
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                raise ValueError("related_field must be a valid JSON list")
        return v

class JobPostCreate(JobPostBase):
    pass

class JobPostUpdate(BaseModel):
    main_field: Optional[str] = None
    num_posts: Optional[int] = None
    related_field: Optional[List[Dict[str, Any]]] = None

class JobPostRead(JobPostBase):
    id: int

    class Config:
        orm_mode = True

class JobPostList(BaseModel):
    items: List[JobPostRead]
