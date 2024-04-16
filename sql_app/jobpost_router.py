import json
from sqlalchemy import func, text
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

from . import crud, models, schemas, database

router = APIRouter(prefix='/jobposts', tags=['jobposts'])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.JobPostRead)
def create_job_post(job_post: schemas.JobPostCreate, db: Session = Depends(get_db)):
    return crud.create_job_post(db=db, job_post=job_post)


@router.get("/{job_post_id}", response_model=schemas.JobPostRead)
def read_job_post(job_post_id: int, db: Session = Depends(get_db)):
    db_job_post = crud.get_job_post(db, job_post_id=job_post_id)
    if db_job_post is None:
        raise HTTPException(status_code=404, detail="JobPost not found")
    return db_job_post


@router.get("/", response_model=list[schemas.JobPostRead])
def read_job_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    job_posts = crud.get_job_posts(db, skip=skip, limit=limit)
    return job_posts


@router.put("/{job_post_id}", response_model=schemas.JobPostRead)
def update_job_post(job_post_id: int, job_post: schemas.JobPostUpdate, db: Session = Depends(get_db)):
    return crud.update_job_post(db=db, job_post_id=job_post_id, updates=job_post)


@router.delete("/clear-data")
def clear_data(db: Session = Depends(get_db)):
    try:
        db.query(models.JobPost).delete()

        sequence_name = "job_posts_id_seq"
        db.execute(text(f"ALTER SEQUENCE {sequence_name} RESTART WITH 1"))

        db.commit()
        return {"message": "모든 데이터가 성공적으로 제거되었습니다."}
    except Exception as e:
        db.rollback()
        return {"error": str(e)}


@router.delete("/{job_post_id}", response_model=dict)
def delete_job_post(job_post_id: int, db: Session = Depends(get_db)):
    if crud.delete_job_post(db=db, job_post_id=job_post_id):
        return {"detail": "JobPost deleted"}
    raise HTTPException(status_code=404, detail="JobPost not found")