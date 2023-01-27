import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
from gensim.models.word2vec import Word2Vec
from konlpy.tag import Okt
import re
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from gensim.models import Word2Vec


def removeNonAscii(s):
    # return "".join(i for i in s if  ord(i)<128)
    Ascii_data = ""
    for i in s:
        if type(i) != float:
            Ascii_data.join(i)

    return Ascii_data



def remove_stop_words(text):
    stopwords = ['으로', '하다', '에서', '오다', '불다', '있다', '주다', '추다', '되다', '저자',
                 '의지', '보고', '통해', '겪다', '이다','거야', '보다', '해도', '안다', '선사',
                  '사이', '남다', '없다', '면서','것이']

    okt = Okt()
    tokenized_data = []
    temp_X = okt.nouns(text)  # 토큰화
    temp_X = [word for word in temp_X if not word in stopwords]  # 불용어 제거
    # 한글자 언어 제거 (적용이 되지 않아 각주처리)
    # for i, v in enumerate(temp_X):
    #     if len(v) == 1:
    #         del temp_X[i]

    tokenized_data.append(temp_X)

    return tokenized_data

def remove_html(text):
    html_pattern = re.compile('<.*?>')
    return html_pattern.sub(r'', text)


def remove_punctuation(text):
    tokenizer = RegexpTokenizer(r'[가-힣]')
    text = tokenizer.tokenize(text)
    text = " ".join(text)
    return text




# 단어 벡터의 평균 구하기
def get_document_vectors(document_list, word2vec_model):
    document_embedding_list = []

    # 각 문서에 대해서
    for line in document_list:
        doc2vec = None
        count = 0
        for word in line.split():
            if word in word2vec_model.wv.vocab:
                count += 1
                # 해당 문서에 있는 모든 단어들의 벡터값을 더한다.
                if doc2vec is None:
                    doc2vec = word2vec_model[word]
                else:
                    doc2vec = doc2vec + word2vec_model[word]

        if doc2vec is not None:
            # 단어 벡터를 모두 더한 벡터의 값을 문서 길이로 나눠준다.
            doc2vec = doc2vec / count
            document_embedding_list.append(doc2vec)

    # 각 문서에 대한 문서 벡터 리스트를 리턴
    return document_embedding_list


# 추천 시스템 구현
def recommendations(title, cosine_similarities):

    df = pd.read_csv('book_txt2.csv')
    books = df[['title', 'summery_list']]

    # 책의 제목을 입력하면 해당 제목의 인덱스를 리턴받아 idx에 저장.
    indices = pd.Series(df.index, index = df['title']).drop_duplicates()
    idx = indices[title]

    # 입력된 책과 줄거리(document embedding)가 유사한 책 5개 선정.
    sim_scores = list(enumerate(cosine_similarities[idx]))
    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)
    sim_scores = sim_scores[1:6]

    return sim_scores

