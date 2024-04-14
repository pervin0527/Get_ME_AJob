from models import Jobkorea, Saramin, FieldAnal, CVDetail, NLPDetail
from datetime import datetime
from database import SessionLocal
import pandas as pd
import random

db = SessionLocal()

jobkorea_db = pd.read_csv('./outputs/jobkorea.csv')

for i in range(len(jobkorea_db)):
    elem = jobkorea_db.loc[i]
    company = elem['회사명']
    title = elem['채용공고 제목']
    options = elem['채용공고 세부 사항']
    techs = elem['기술 세부 사항']
    link = elem['링크']
    create_date = datetime.now()

    q = Jobkorea(company=company, title=title, options=options, techs=techs, link=link, create_date=create_date)
    db.add(q)

saramin_db = pd.read_csv('./outputs/saramin.csv')

for i in range(len(saramin_db)):
    elem = saramin_db.loc[i]
    company = elem['회사명']
    title = elem['채용공고 제목']
    options = elem['채용공고 세부 사항']
    techs = elem['기술 세부 사항']
    link = elem['링크']
    create_date = datetime.now()

    q = Saramin(company=company, title=title, options=options, techs=techs, link=link, create_date=create_date)
    db.add(q)

for i in range(50):
    field = f'{i}'
    count = random.random() * i

    q = FieldAnal(field=field, count=count)
    db.add(q)

for i in range(10):
    skill = f'{i}'
    count = random.random() * i

    q = CVDetail(skill=skill, count=count)
    db.add(q)

for i in range(10):
    skill = f'{i}'
    count = random.random() * i

    q = NLPDetail(skill=skill, count=count)
    db.add(q)

db.commit()

