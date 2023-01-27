import urllib.request
import pandas as pd
import numpy as np
import requests
from io import BytesIO
from nltk.tokenize import RegexpTokenizer
import nltk
from gensim.models import Word2Vec, KeyedVectors
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
from funtion import *
import seaborn as sns
import gensim

df = pd.read_csv("book_txt.csv")
df_long_list = df["summery_list"].str.len().tolist()

df = df.dropna(axis=0)

# 불용어 처리하여 df['cleaned'] 에 저장
# 참고 : https://mr-doosun.tistory.com/24

df['cleaned'] = df['summery_list'].apply(remove_stop_words)

df['cleaned'].replace('', np.nan, inplace=True)
df = df[df['cleaned'].notna()]


corpus = []
for words in df['cleaned']:
    words = sum(words, [])
    corpus.append(words)


# 사전훈련된 워드 임베딩 사용하기
