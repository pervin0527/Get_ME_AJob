import pandas as pd

from src.saramin import SaraminCrawler
from src.jobkorea import JobKoreaCrawler

from utils.util import save_dataset
from src.data_process import preprocessing

from models import Jobkorea, Saramin, JobPost
from datetime import datetime
from database import SessionLocal

def main():
    '''
    # 시간이 너무 많이 걸려서 주석처리 후 수행
    ## 잡코리아 크롤링
    jobkorea_crawler = JobKoreaCrawler()
    jobkorea_dataset = jobkorea_crawler.crawling()
    save_dataset("./outputs/", "jobkorea", jobkorea_dataset)
    
    ## 사람인 크롤링
    saramin_crawler = SaraminCrawler()
    saramin_dataset = saramin_crawler.crawling()
    save_dataset("./outputs/", "saramin", saramin_dataset)
    '''

    jobkorea_df = pd.read_csv('./outputs/jobkorea.csv')
    saramin_df = pd.read_csv('./outputs/saramin.csv')
    
    preprocessing(jobkorea_df, saramin_df)

    db = SessionLocal()

    # output 파일 읽어오기
    jobkorea_df = pd.read_csv('./outputs/jobkorea.csv')
    saramin_df = pd.read_csv('./outputs/saramin.csv')
    pp_df = pd.read_csv('test.csv')

    for i in range(len(jobkorea_df)):
        elem = jobkorea_df.loc[i]
        company = elem['회사명']
        title = elem['채용공고 제목']
        options = elem['채용공고 세부 사항']
        techs = elem['기술 세부 사항']
        link = elem['링크']
        create_date = datetime.now()

        q = Jobkorea(company=company, title=title, options=options, techs=techs, link=link, create_date=create_date)
        db.add(q)

    for i in range(len(saramin_df)):
        elem = saramin_df.loc[i]
        company = elem['회사명']
        title = elem['채용공고 제목']
        options = elem['채용공고 세부 사항']
        techs = elem['기술 세부 사항']
        link = elem['링크']
        create_date = datetime.now()

        q = Saramin(company=company, title=title, options=options, techs=techs, link=link, create_date=create_date)
        db.add(q)

    for i in range(len(pp_df)):
        elem = pp_df.loc[i]
        main_field = elem['주요분야']
        num_posts = int(elem['공고수'])
        related_field = elem['연관분야']

        q = JobPost(main_field=main_field, num_posts=num_posts, related_field=related_field)
        db.add(q)

    db.commit()
    
if __name__ == "__main__":
    SAVE_PATH = "./outputs"
    KEYWORD = '딥러닝'
    WAIT_SEC = 3
    TOTAL_SCROLL = 100
    DEBUG = False

    main()