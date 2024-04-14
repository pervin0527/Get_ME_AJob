# DB에서 데이터를 가져오거나 입력하는 역할을 수행

from models import Jobkorea, Saramin, FieldAnal
from sqlalchemy.orm import Session

def get_jobkorea_list(db: Session):
    jobkorea_list = db.query(Jobkorea)\
        .order_by(Jobkorea.create_date.desc())\
        .all()
    return jobkorea_list

def get_saramin_list(db: Session):
    saramin_list = db.query(Saramin)\
        .order_by(Saramin.create_date.desc())\
        .all()
    return saramin_list

def get_field_anal_list(db: Session):
    field_anal_list = db.query(FieldAnal).order_by(FieldAnal.id.desc()).all()
    return field_anal_list

def get_data_detail(db: Session, data_id: str):
    id_list = data_id.split('_')
    db_name = id_list[0]
    id = int(id_list[2])
    if db_name == 'jobkorea':
        data_detail = db.query(Jobkorea).get(id)

    else :
        data_detail = db.query(Saramin).get(id)

    return data_detail

def get_field_detail(db: Session, data_id: str):
    id_list = data_id.split('_')
    id = int(id_list[2])
    data_detail = db.query(FieldAnal).get(id)

    return data_detail