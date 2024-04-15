# crud를 통해 DB에서 데이터를 가져올 때 적절한 형식을 맞춰서 가져오는지 검사할 때 사용
# 미리 데이터들의 형태를 정의해둔다.

import datetime

from pydantic import BaseModel


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

class FA(BaseModel):
    id: int
    field: str
    cnt: int
    related: str

    class Config:
        orm_mode = True