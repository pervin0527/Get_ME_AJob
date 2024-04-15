## uvicorn sql_app.main:app --reload
import os
import json
import pandas as pd

import matplotlib
matplotlib.use('Agg')

import seaborn as sns
import matplotlib.pyplot as plt

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from sqlalchemy import func, text

from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from . import models, schemas
from .database import SessionLocal, engine
from .jobpost_router import router as jp_router

from src.saramin import SaraminCrawler
from src.jobkorea import JobKoreaCrawler
from src.data_process import preprocessing


WAIT_SEC = 3
DEBUG = True
models.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(jp_router)

CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
STATIC_DIR = os.path.join(CURRENT_DIR, "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

scheduler = AsyncIOScheduler()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def draw_main_graph(names, counts, filepath):
    counts = [int(x) for x in counts]
    plt.figure(figsize=(16, 8))
    sns.barplot(x=names, y=counts, palette='viridis')
    plt.title('주요분야별 채용공고 수')
    plt.xlabel('채용공고 수')
    plt.ylabel('주요분야')
    plt.savefig(filepath)  # 파라미터로 받은 경로에 저장
    plt.close()


async def load_data():
    jobkorea_crawler = JobKoreaCrawler(WAIT_SEC, DEBUG)
    saramin_crawler = SaraminCrawler(WAIT_SEC, DEBUG)

    jobkorea_dataset = jobkorea_crawler.crawling()
    saramin_dataset = saramin_crawler.crawling()

    total_df = preprocessing(jobkorea_dataset, saramin_dataset)
    total_df.columns = ['main_field', 'num_posts', 'related_field']

    # total_df['related_field'] = total_df['related_field'].apply(lambda x: json.dumps(x))
    total_df = total_df[total_df['main_field'] != 'Unknown']
    total_df['related_field'] = total_df['related_field'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)
    draw_main_graph(total_df['main_field'].to_list(), total_df['num_posts'].to_list(), f"{STATIC_DIR}/graph_main.png")

    db = SessionLocal()
    existing_data = pd.read_sql(sql="SELECT main_field, num_posts, related_field FROM job_posts", con=db.bind)
    existing_data['related_field'] = existing_data['related_field'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)

    if existing_data.empty:
        for index, row in total_df.iterrows():
            job_post = schemas.JobPostCreate(
                main_field=row['main_field'],
                num_posts=row['num_posts'],
                related_field=row['related_field']
            )
            db.add(models.JobPost(**job_post.dict()))
    else:
        merged_data = pd.merge(total_df, existing_data, on=["main_field", "related_field"], suffixes=('_new', '_existing'), how='outer', indicator=True)
        update_data = merged_data[(merged_data['_merge'] == 'both') & (merged_data['num_posts_new'] != merged_data['num_posts_existing'])]
        for index, row in update_data.iterrows():
            db.query(models.JobPost).filter(models.JobPost.main_field == row['main_field'], models.JobPost.related_field == row['related_field']).update({'num_posts': row['num_posts_new']})

        new_data = merged_data[merged_data['_merge'] == 'left_only']
        for index, row in new_data.iterrows():
            job_post = schemas.JobPostCreate(
                main_field=row['main_field'],
                num_posts=row['num_posts_new'],
                related_field=row['related_field']
            )
            db.add(models.JobPost(**job_post.dict()))

    db.commit()
    db.close()


@app.on_event("startup")
async def startup_event():
    await load_data()
    
    scheduler.add_job(
        func=load_data,
        # trigger=CronTrigger(minute='*/3'), ## 3분
        # trigger=CronTrigger(hour='*/10'), ## 1시간
        trigger=CronTrigger(hour=0, minute=0), ## 매일 밤 12시
        timezone="Asia/Seoul"
    )
    scheduler.start()
    scheduler.print_jobs()


@app.get("/", response_class=HTMLResponse)
async def read_main():
    with open(os.path.join(f"{STATIC_DIR}", "index.html"), "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)


@app.on_event("shutdown")
async def shutdown_event():
    db = next(get_db())
    db.query(models.JobPost).delete()
    sequence_name = "job_posts_id_seq"
    db.execute(text(f"ALTER SEQUENCE {sequence_name} RESTART WITH 1"))
    db.commit()
    db.close()