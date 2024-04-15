import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from seaborn import sns

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import FileResponse
from starlette.staticfiles import StaticFiles

from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.asyncio import AsyncIOScheduler

import models, schemas

from domain.data import data_router

from src.saramin import SaraminCrawler
from src.jobkorea import JobKoreaCrawler
from src.data_process import preprocessing

from database import SessionLocal

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(data_router.router)
app.mount("/assets", StaticFiles(directory="frontend/dist/assets"))

# 그래프 생성
def draw_main_graph(names, counts, filepath):
    counts = [int(x) for x in counts]
    plt.figure(figsize=(16, 8))
    sns.barplot(x=names, y=counts, palette='viridis')
    plt.title('주요분야별 채용공고 수')
    plt.xlabel('채용공고 수')
    plt.ylabel('주요분야')
    plt.savefig(filepath)  # 파라미터로 받은 경로에 저장
    plt.close()


def draw_sub_graph(related_fields, keyword, filepath):    
    fields = [list(field.keys())[0] for field in related_fields]
    counts = [list(field.values())[0] for field in related_fields]
    
    plt.figure(figsize=(12, 8))
    sns.barplot(x=fields, y=counts, palette='viridis')
    plt.title(f'Top 10 Related Fields for {keyword}')
    plt.ylabel('Counts')
    plt.xticks(rotation=45)
    plt.savefig(filepath)
    plt.close()



@app.on_event("startup")
async def load_data():
    jobkorea_crawler = JobKoreaCrawler(3)
    saramin_crawler = SaraminCrawler(3)

    # 크롤링, 결과를 dataframe형태로 전환
    jobkorea_dataset = jobkorea_crawler.crawling()
    saramin_dataset = saramin_crawler.crawling()
    print('good0')
    jobkorea_df = pd.DataFrame(jobkorea_dataset)
    saramin_df = pd.DataFrame(saramin_dataset)
    print('good00')
    jobkorea_df.to_csv('jobkorea.csv', encoding='utf-8')
    saramin_df.to_csv('saramin.csv', encoding='utf-8')
    
    # 전처리
    total_df = preprocessing(jobkorea_df, saramin_df)
    total_df.columns = ['main_field', 'num_posts', 'related_field']
    print('good1')

    # total_df['related_field'] = total_df['related_field'].apply(lambda x: json.dumps(x))
    total_df = total_df[total_df['main_field'] != 'Unknown']
    total_df['related_field'] = total_df['related_field'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)
    print('good2')

    # 기존 db호출
    db = SessionLocal()
    existing_data = pd.read_sql(sql="SELECT main_field, num_posts, related_field FROM job_posts", con=db.bind)
    existing_data['related_field'] = existing_data['related_field'].apply(lambda x: json.dumps(x) if isinstance(x, list) else x)
    print('good3')

    # db가 비어있는지 확인
    if existing_data.empty: # db가 비어있는 경우 -> 그냥 데이터 입력
        print('good4')
        for index, row in total_df.iterrows():
            job_post = schemas.JobPostCreate(
                main_field=row['main_field'],
                num_posts=row['num_posts'],
                related_field=row['related_field']
            )
            db.add(models.JobPost(**job_post.dict()))
            print('good5')
    else: # db에 데이터가 있는 경우 -> 비교해서 달라진 데이터만 입력
        merged_data = pd.merge(total_df, existing_data, on=["main_field", "related_field"], suffixes=('_new', '_existing'), how='outer', indicator=True)
        print('good6')
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
        print('good7')

    db.commit()
    db.close()
    print('good8')

scheduler = AsyncIOScheduler()

@app.get("/")
def index():
    return FileResponse("frontend/dist/index.html")