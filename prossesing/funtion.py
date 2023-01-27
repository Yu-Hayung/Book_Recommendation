from konlpy.tag import *
import pandas as pd
import csv
import re


def Kma_nouns_out(txt):
    Kma = Kkma()  # Okt 객체 선언
    nouns = Kma.nouns(txt)  # 명사 배열

    # 1글자 명사(불용어) 삭제
    return_list = []
    for i in nouns:
        if len(i) != 1:
            return_list.append(i)

    return return_list

def KOM_nouns_out(txt):
    Kom = Komoran()  # Okt 객체 선언
    nouns = Kom.nouns(txt)  # 명사 배열

    # 1글자 명사(불용어) 삭제
    return_list = []
    for i in nouns:
        if len(i) != 1:
            return_list.append(i)

    return return_list


def OKT_nouns_out(txt): # 명사추출 함수
    okt = Okt()  # Okt 객체 선언
    nouns = okt.nouns(txt)  # 명사 배열

    #1글자 명사(불용어) 삭제
    return_list = []
    for i in nouns:
        if len(i) != 1:
            return_list.append(i)

    return return_list


def compare_list_set(list1, list2):
    for i in list2:
        count_num = list1.count(i)
        if count_num == 0:
            list1.append(i)

    return list1


def cound_nouns_dic(list1):
    dic = {}
    for i in list1:
        dic[i] = list1.count(i)

    return dic


def jaccard_similarity(x, y):
    intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))

    return intersection_cardinality / float(union_cardinality)


def find_kr(str):
    re_str = re.compile('[가-힣]+').findall(str)
    return re_str

def word_remove(words):
    if '방법' in words:
        words.remove('방법')
    if '무엇' in words:
        words.remove('무엇')
    if '대중' in words:
        words.remove('대중')
    if '사람' in words:
        words.remove('사람')
    if '공부' in words:
        words.remove('공부')
    if '유행' in words:
        words.remove('유행')
    if '문제' in words:
        words.remove('문제')


    return words