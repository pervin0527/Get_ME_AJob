## uvicorn sql_app.main:app --reload
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/jobposts/", response_model=schemas.JobPostRead)
def create_job_post(job_post: schemas.JobPostCreate, db: Session = Depends(get_db)):
    return crud.create_job_post(db=db, job_post=job_post)

@app.get("/jobposts/{job_post_id}", response_model=schemas.JobPostRead)
def read_job_post(job_post_id: int, db: Session = Depends(get_db)):
    db_job_post = crud.get_job_post(db, job_post_id=job_post_id)
    if db_job_post is None:
        raise HTTPException(status_code=404, detail="JobPost not found")
    return db_job_post

@app.get("/jobposts/", response_model=list[schemas.JobPostRead])
def read_job_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    job_posts = crud.get_job_posts(db, skip=skip, limit=limit)
    return job_posts

@app.put("/jobposts/{job_post_id}", response_model=schemas.JobPostRead)
def update_job_post(job_post_id: int, job_post: schemas.JobPostUpdate, db: Session = Depends(get_db)):
    return crud.update_job_post(db=db, job_post_id=job_post_id, updates=job_post)

@app.delete("/jobposts/{job_post_id}", response_model=dict)
def delete_job_post(job_post_id: int, db: Session = Depends(get_db)):
    if crud.delete_job_post(db=db, job_post_id=job_post_id):
        return {"detail": "JobPost deleted"}
    raise HTTPException(status_code=404, detail="JobPost not found")
