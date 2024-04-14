# url에 부합하는 역할을 수행한다.
# 미리 만들어둔 crud파일의 함수를 사용해서 DB에서 데이터를 가져오고 출력한다.

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from domain.data import data_schema, data_crud

router = APIRouter(
    prefix="/api/data",
)


@router.get("/jobkorea_list", response_model=list[data_schema.Jobkorea])
def jobkorea_list(db: Session = Depends(get_db)):
    _jobkorea_list = data_crud.get_jobkorea_list(db)
    return _jobkorea_list

@router.get("/saramin_list", response_model=list[data_schema.Saramin])
def saramin_list(db: Session = Depends(get_db)):
    _saramin_list = data_crud.get_saramin_list(db)
    return _saramin_list

@router.get("/jobkorea_detail/{jobkorea_id}", response_model=data_schema.Jobkorea)
def jobkorea_detail(jobkorea_id: int, db: Session = Depends(get_db)):
    jobkorea_detail = data_crud.get_jobkorea_detail(db, jobkorea_id=jobkorea_id)
    return jobkorea_detail

@router.get("/saramin_detail/{saramin_id}", response_model=data_schema.Saramin)
def saramin_detail(saramin_id: int, db: Session = Depends(get_db)):
    saramin_detail = data_crud.get_saramin_detail(db, saramin_id=saramin_id)
    return saramin_detail

@router.get('/data_detail/{data_id}', response_model=data_schema.Detail)
def data_detail(data_id: str, db: Session=Depends(get_db)):
    data_detail = data_crud.get_data_detail(db, data_id=data_id)
    return data_detail

@router.get('/field_anal', response_model=list[data_schema.FA])
def field_anal(db: Session = Depends(get_db)):
    _field_anal = data_crud.get_field_anal_list(db)
    return _field_anal