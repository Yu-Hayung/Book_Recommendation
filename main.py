from funtion import *
from find_keyword import *
from math import *


txt = "어른이 되면 무엇이든 다 될 줄 알았다"

keyword_list = find_keyword(txt, n_gram_range=(2, 2))[1]
book_df = pd.read_csv('book_txt.csv')
Recommendation = []

print('======================   keyword_list   ====================================')
print(f'keyword_list  > {keyword_list}')

Recommendation_df_1 = pd.DataFrame(columns=['title_list', 'publisher_list', 'Author_list', 'introduction_list', 'url_list', 'summery_list', 'keyword_list'])

words = []
for i in keyword_list:
    word_list = str(i).split(' ')
    for j in word_list:
        words.append(j)
words = list(set(words))

join_words = '|'.join(words)     # .str.contains 여러개 담기위한 '|' 처리

Recommendation_df_2 = book_df[book_df['keyword_list'].str.contains(join_words)]
Recommendation_df_fin = pd.concat([Recommendation_df_1, Recommendation_df_2])

Recommendation_df_fin = Recommendation_df_fin.drop_duplicates(subset='title_list')


if len(Recommendation_df_fin) >= 1:
    Recommendation = Recommendation_df_fin.to_dict('records')

    num = 0
    for Recom_book_data in Recommendation:

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


        if Recommended_txt_similarity > 0.0:
            num += 1
            print(
            f'==== {num} ============================================ \n'
            f'텍스트 : {txt} \n'
            f'텍스트 키워드 : {words} \n'
            f'책 제목 : {Recom_book_data["title_list"]} \n'
            f'작가 : {Recom_book_data["Author_list"]} \n'
            f'출판사 : {Recom_book_data["publisher_list"]} \n'
            f'줄거리 : {Recom_book_data["summery_list"]} \n'
            f'줄거리 키워드 : {word_list2}\n'
            f'유사도 : {str(Recommended_txt_similarity)}'
            )

        # csv 저장하기
        f = open('data_save.csv', 'a', newline='', encoding='utf8')
        wr = csv.writer(f)
        wr.writerow([str(txt), words,
                     str(Recom_book_data["title_list"]), str(Recom_book_data["summery_list"]),
                     str(Recom_book_data["keyword_list"]), str(Recommended_txt_similarity)])
        f.close()


else:
    print('추천 도서 없음')



