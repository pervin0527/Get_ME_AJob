import re
import pandas as pd

from src.util import plot_top_keywords, plot_related_keywords

FILTER_LIST = ['딥러닝', '인공지능', '머신러닝', '1', '']
NLP_LIST = ['자연어처리(NLP)', '챗봇', '음성인식', 'NLP(자연어처리)']
CV_LIST = ['이미지프로세싱', '영상처리', 'OpenCV', '컴퓨터비전']
BACKEND_LIST = ['백엔드/서버개발','웹개발', '웹표준·웹접근성', 'DB튜닝','DBA', '유지보수', 'Spring', 'SpringBoot', '클라이언트', '모바일앱개발', 'API', '서버구축', '웹마스터', 'RestAPI', 'DBMS', '서버관리']
DATA_ENGINEER_LIST = [ '데이터분석가','데이터엔지니어','데이터분석', '빅데이터', 'R', '분석모델링', '데이터시각화', '데이터레이크', 'DataMining','데이터라벨링', 'BigData']
EMBEDDED_LIST = ['펌웨어', 'IoT', 'H/W', '임베디드']
SECURITY_LIST =['정보보안', '암호화폐', '보안컨설팅', '보안관제', '방화벽', '네트워크관리', '블록체인']



def split_sentence(sentence):
    """주어진 문장을 쉼표로 분리하고 공백을 제거하여 중복되지 않는 단어 목록을 반환."""
    vocabs = []
    words = sentence.split(',')
    for word in words:
        word = word.strip()
        if word not in vocabs and word not in FILTER_LIST:
            vocabs.append(word)
    return vocabs

def preprocessing_skills(sentence):
    sentence = re.sub(r"[\[\]-]", "", sentence)
    sentence = re.sub(r"\([^)]*\)", "", sentence)
    # 숫자와 점 사이에 공백 추가
    sentence = re.sub(r"(\d)\.", r"\1. ", sentence)
    # 연속된 공백 정리
    sentence = re.sub(r"\s+", " ", sentence)
    # 점을 쉼표로 치환
    sentence = re.sub(r"\. ", ", ", sentence)
    sentence = sentence.strip()

    # 분리된 단어들을 통해 빈도 사전 업데이트
    vocab_list = split_sentence(sentence)
    return vocab_list

def build_vocabs(skill_list):
    vocabs = {}
    for skills in skill_list:
        for word in skills:
            word = word.strip()
            if word in vocabs:
                vocabs[word] += 1
            else:
                vocabs[word] = 1
    return vocabs


def build_main_fields(top_vocabs):
    """ 각 단어를 해당 분야로 맵핑하는 함수 """
    keyword_to_field_dict = {}
    for word, _ in top_vocabs:
        if word in NLP_LIST:
            keyword_to_field_dict[word] = 'NLP'
        elif word in CV_LIST:
            keyword_to_field_dict[word] = 'CV'
        elif word in BACKEND_LIST:
            keyword_to_field_dict[word] = 'Backend'
        elif word in DATA_ENGINEER_LIST:
            keyword_to_field_dict[word] = 'Data Engineer'
        elif word in EMBEDDED_LIST:
            keyword_to_field_dict[word] = 'Embedded'
        elif word in SECURITY_LIST:
            keyword_to_field_dict[word] = 'Security'
        else:
            keyword_to_field_dict[word] = 'Unknown'  # 기타 분야
    return keyword_to_field_dict

# input : (기술 세부사항) => output : 분야 리스트 | ex) "이미지 프로세싱, 인공지능" => ['CV']
def apply_main_fields(skills, keyword_to_field_dict):
    new_detail_skills = set()
    for skill in skills:
        skill = skill.strip()
        field = keyword_to_field_dict.get(skill, 'Unknown')  # 딕셔너리에서 분야를 가져오되, 없다면 'Other'
        new_detail_skills.add(field)
    return list(new_detail_skills)  


def build_sentece_vocabs(skills):
    sentence_vocabs = []

    for sentence in skills:
        words = sentence.split(',')
        sent_vocabs = []

        for word in words:
            word = word.strip()
            if word not in FILTER_LIST:
                sent_vocabs.append(word)

        sentence_vocabs.append(sent_vocabs)

    return sentence_vocabs


def build_related_fields(word, sentence_vocabs):
    related_words_dict = {}

    for sent_words_list in sentence_vocabs:
        # 해당 단어가 있으면
        if word in sent_words_list:
            for w in sent_words_list:
                if w != word:
                    if w in related_words_dict:
                        related_words_dict[w] += 1
                    else:
                        related_words_dict[w] = 1

    return related_words_dict

def create_field_counter(total_df):
    field_counter = {
        'NLP': 0,
        'CV': 0,
        'Backend': 0,
        'Data Engineer': 0,
        'Embedded': 0,
        'Security': 0,
    }

    for fields in total_df['분야'].tolist():
        for field in fields:
            field = field.strip()
            if field in field_counter:
                field_counter[field] += 1

    return field_counter

def create_skill_counter(vocabs):
    related_skill_counter = {
        'NLP': {},
        'CV': {},
        'Backend': {},
        'Data Engineer': {},
        'Embedded': {},
        'Security': {},
    }

    for nlp_skill in NLP_LIST:

        if nlp_skill in vocabs:  # 키가 있는지 확인
            related_skill_counter['NLP'][nlp_skill] = vocabs[nlp_skill]
    for cv_skill in CV_LIST:
        if cv_skill in vocabs:  # 키가 있는지 확인
            related_skill_counter['CV'][cv_skill] = vocabs[cv_skill]

    for backend_skill in BACKEND_LIST:
        if backend_skill in vocabs:  # 키가 있는지 확인
            related_skill_counter['Backend'][backend_skill] = vocabs[backend_skill]

    for data_engineer_skill in DATA_ENGINEER_LIST:
        if data_engineer_skill in vocabs:  # 키가 있는지 확인
            related_skill_counter['Data Engineer'][data_engineer_skill] = vocabs[data_engineer_skill]

    for embedded_skill in EMBEDDED_LIST:
        if embedded_skill in vocabs:  # 키가 있는지 확인
            related_skill_counter['Embedded'][embedded_skill] = vocabs[embedded_skill]

    for security_skill in SECURITY_LIST:
        if security_skill in vocabs:  # 키가 있는지 확인
            related_skill_counter['Security'][security_skill] = vocabs[security_skill]

    return related_skill_counter

def create_db_dataframe(field_counter, related_skill_counter):
    db_features={
        "주요분야":[],
        "공고 수":[],
        "연관 분야":[]
    }

    for key, values in field_counter.items():

        db_features['주요분야'].append(key)
        db_features['공고 수'].append(values) 
        db_features['연관 분야'].append(related_skill_counter[key])

    final_df = pd.DataFrame(db_features)
    return final_df

def preprocessing(*args):

    total_df = pd.concat(args)
    total_df['회사명'] = total_df['회사명'].str.replace(r"\(.*?\)|\([^)]*$|㈜", "", regex=True).str.strip()
        
    ## 회사명이 같더라도 채용공고 제목이 다를 수 있음. -> 회사명과 채용공고 제목이 같으면 동일한 공고로 취급하고 삭제.    
    if '채용공고 제목' in total_df.columns:
        total_df = total_df.drop_duplicates(subset=['회사명', '채용공고 제목'], keep='first')

    # 기술 세부사항 열 리스트로 변경
    total_df['기술 세부 사항'] = total_df['기술 세부 사항'].apply(preprocessing_skills)

    ## 단어 사전 생성, 단어 빈도수 측정.
    vocabs = build_vocabs(total_df['기술 세부 사항'].tolist())
    sorted_vocabs_list = sorted(vocabs.items(), key=lambda x: x[1], reverse=True)

    top100_vocabs = sorted_vocabs_list[:100]
    top30_vocabs = sorted_vocabs_list[:30]
    plot_top_keywords(top30_vocabs, "Top 30 Keywords", 30)
    plot_top_keywords(top100_vocabs, "Top 100 Keywords", 100)

    main_fields_dict = build_main_fields(top100_vocabs)
    total_df['분야'] = total_df['기술 세부 사항'].apply(lambda x: apply_main_fields(x, main_fields_dict))
    
    '''
    # 공통 기술 세부 사항(LIKE 인공지능) 단어 제거 
    sentence_vocabs = build_sentece_vocabs(total_df['기술 세부 사항'].to_list())

   
    for idx, (word, cnt) in enumerate(top30_vocabs):
        related_field_dict = build_related_fields(word, sentence_vocabs)
        plot_related_keywords(word, related_field_dict, idx)

    '''

    field_counter = create_field_counter(total_df=total_df)
    related_skill_counter = create_skill_counter(vocabs)
    db_df = create_db_dataframe(field_counter, related_skill_counter)

    return db_df
    
    
    

