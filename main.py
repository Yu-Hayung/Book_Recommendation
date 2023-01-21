from funtion import *
from find_keyword import *
from math import *

import pandas as pd
import json
import os, random


json_path = 'C:/Users/HERO/Downloads/022.요약문 및 레포트 생성 데이터/01.데이터/1.Training/라벨링데이터/TL1/03.his_cul/2~3sent'
path = os.listdir(json_path)


answer_list = []

for i in path:
    path_data = json_path + '/' + i

    with open(path_data, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

        summary = json_data['Annotation']['summary1']
        answer_list.append(str(summary))

print('질문 데이터 개수 :', len(answer_list))

count2 = 0
for txt in answer_list:
    keyword_list = find_keyword(txt, n_gram_range=(1, 4))[1]
    book_df = pd.read_csv('book_txt.csv')
    Recommendation = []

    # print('======================   keyword_list   ====================================')
    # print(f'txt : {txt}')
    # print(f'keyword_list  > {keyword_list}')

    Recommendation_df_1 = pd.DataFrame(columns=['title_list', 'publisher_list', 'Author_list', 'introduction_list', 'url_list', 'summery_list', 'keyword_list'])

    words = []
    for i in keyword_list:
        word_list = str(i).split(' ')
        for j in word_list:
            words.append(j)

    words = list(set(words))
    words = word_remove(words) # 지정단어 삭제


    join_words = '|'.join(words)     # .str.contains 여러개 담기위한 '|' 처리

    Recommendation_df_2 = book_df[book_df['keyword_list'].str.contains(join_words)]
    Recommendation_df_fin = pd.concat([Recommendation_df_1, Recommendation_df_2])

    Recommendation_df_fin = Recommendation_df_fin.drop_duplicates(subset='title_list')

    Recommendation_save_dic = {}
    count = 0
    if len(Recommendation_df_fin) != 0:
        while True:
            Recommendation = Recommendation_df_fin.to_dict('records')
            try:
                random_num = random.randrange(0, len(Recommendation_df_fin))
            except:
                random_num = 0
            # 첫번째 책만 저장 유사도가 높든 낮든 1질문 1책
            while True:
                try:
                    if Recommendation[random_num]:
                        Recom_book_data = Recommendation[random_num]
                        break
                except:
                    continue


            # 책 줄거리 자카드유사도 계산을 위한 형태 맞추기
            words2 = []
            book_keyword_list = find_kr(Recom_book_data["keyword_list"])
            for i in book_keyword_list:
                word_list2 = str(i).split(' ')
                word_list2 = set(word_list2)
                for j in word_list2:
                    words2.append(j)
            word_list2 = list(set(words2))

            Recommended_txt_similarity = jaccard_similarity(words, word_list2)

            try:
                if Recommended_txt_similarity > 0.16:
                    # csv 저장하기

                    print(
                        f'================================================ \n'
                        f'텍스트 : {txt} \n'
                        f'텍스트 키워드 : {words} \n'
                        f'책 제목 : {Recom_book_data["title_list"]} \n'
                        f'작가 : {Recom_book_data["Author_list"]} \n'
                        # f'출판사 : {Recom_book_data["publisher_list"]} \n'
                        # f'줄거리 : {Recom_book_data["summery_list"]} \n'
                        f'줄거리 키워드 : {word_list2}\n'
                        f'유사도 : {str(Recommended_txt_similarity)}'
                    )

                    f = open('data_save.csv', 'a', newline='', encoding='utf8')
                    wr = csv.writer(f)
                    wr.writerow([str(txt), words,
                                 str(Recom_book_data["title_list"]), str(Recom_book_data["summery_list"]),
                                 str(word_list2), str(round(Recommended_txt_similarity, 3))])
                    f.close()
                    count2 += 1
                    print(f'count2 : {count2}')
                    print('저장완료')
                    break
                else:
                    count += 1
                    if count > 100:
                        print('100권 확인후 없음 종결 다음 질문으로 진행')
                        break
                    continue
            except Exception as e:
                pass



    else:
        print("=======================================================================")
        print('len(Recommendation_df_fin) == 0: >', len(Recommendation_df_fin))
        print('추천 도서 없음')
