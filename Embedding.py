import pandas as pd
import matplotlib.pyplot as plt
import urllib.request
from gensim.models.word2vec import Word2Vec
from konlpy.tag import Okt
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer



train_data = pd.read_csv('book_txt.csv')

train_data = train_data.dropna(how = 'any') # Null 값이 존재하는 행 제거
train_data['summery_list'] = train_data['summery_list'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","")

stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다', '계', '에서', '간'
             , '작', '단', '오다', '불다', '있다', '주다', '추다', '그', '되다', '저자', '의지', '보고', '통해', '겪다', '이다'
             ,'거야', '보다', '해도', '안다', '선사', '명','을','액','를','권','머','아','어','응','예','청','인','다시','사이',
             '남다','중','내','다','때','수','없다','면서','세', '것이', '안']

okt = Okt()
tokenized_data = []
for sentence in train_data['summery_list']:
    temp_X = okt.morphs(sentence, stem=True) # 토큰화
    temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
    tokenized_data.append(temp_X)

# 단어가 1개 이하인 샘플의 인덱스를 찾아서 저장하고, 해당 샘플들은 제거.
drop_train = [index for index, sentence in enumerate(tokenized_data) if len(sentence) <= 1]
tokenized_doc = np.delete(tokenized_data, drop_train, axis=0)

tokenizer = Tokenizer()
tokenizer.fit_on_texts(tokenized_doc)
word2idx = tokenizer.word_index
vocab_size = len(word2idx) + 1 # 단어 집합의 크기

# Word2Vec 훈련
from gensim.models import Word2Vec
model = Word2Vec(sentences=tokenized_data, size=100, window=5, min_count=5, workers=4, sg=0)

print('완성된 임베딩 매트릭스의 크기 확인 >>', model.wv.vectors.shape)

# 모델 저장
model.wv.save_word2vec_format("book_recommendation_v1.bin")


'''

https://monetd.github.io/python/nlp/Word-Embedding-Word2Vec-%EC%8B%A4%EC%8A%B5/
한국어Permalink
한국어는 박규병님께서 공개한 Word2Vec 모델이 있다. 해당 깃허브 주소와 모델의 다운로드 링크는 아래와 같다.

GitHub : https://github.com/Kyubyong/wordvectors
모델 다운로드 경로 : https://drive.google.com/file/d/0B0ZXk88koS2KbDhXdWg1Q2RydlU/view
파일의 크기는 약 77MB이고 압축을 풀면 50MV 가량의 ko.bin 파일을 gensim 라이브러리로 로드하면 된다.

import gensim
model = gensim.models.Word2Vec.load('ko.bin 파일의 경로')

'''

