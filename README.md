# 취업시켜조(Get Me A Job)

![main img](./imgs/main.png)

## 1.목표

1. 잡코리아, 사람인 웹사이트에서 `머신러닝 엔지니어`, `딥러닝 엔지니어`를 검색하고 채용공고들을 크롤링한다.
2. 크롤링 데이터를 전처리하여 각 공고에 주요 분야, 연관 분야를 부여한다.
3. 전처리된 데이터를 데이터베이스에 저장.(FastAPI + PostgreSQL)
4. 주요 분야의 수를 그래프로 보여주고, 사용자가 선택한 주요 분야와 연관된 단어들을 그래프로 보여준다.

## 2.설치

### 2-1.파이썬 라이브러리

    ## data
    pip install pandas tqdm seaborn matplotlib

    ## crawling
    pip install selenium webdriver-manager

    ## FastAPI + DB
    pip install fastapi psycopg2 sqlalchemy
    pip install "uvicorn[standard]"

### 2-2.PostgreSQL

[https://www.postgresql.org/](https://www.postgresql.org/)에서 DB 설치.

    ## 터미널에서 DB로 접속.
    psql postgres

    ## 비밀번호 설정 및 재시작.
    CREATE ROLE postgres WITH LOGIN PASSWORD '비밀번호';

    brew services restart postgresql ## MacOS

    net stop postgresql-xx ## Windows
    net start postgresql-xx



    CREATE DATABASE '테이블 이름';
    \connect '테이블 이름';

    ## sql_app/database.py에서 DB 연결 수정.
    SQLALCHEMY_DATABASE_URL = "postgresql://USERNAME:PASSWORD@localhost/TABLENAME"

## 3.실행

    uvicorn sql_app.main:app --reload
