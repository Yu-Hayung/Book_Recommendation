# 라이브러리 준비하기
import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd
from find_keyword import *

num = 0

Category_list = [
   'http://www.yes24.com/24/Category/Display/001001003022?PageNumber='
]

for i in range(50):
   num += 1
   url = f"http://www.yes24.com/24/Category/Display/001001047010?PageNumber={num}"

   # 웹 서버에 요청하기
   res = requests.get(url)
   res.raise_for_status()

   # soup 객체 만들기
   soup = BeautifulSoup(res.text, "lxml")

   title_list = []
   publisher_list = []
   Author_list = []
   introduction_list = []
   url_list = []
   summery_list = []
   keyword_list = []

      # title_list
   content = soup.find_all('ul', {'class':'clearfix'})
   itme = content[0].find_parent('div'), {'class': 'gd_nameF'}
   publisher = soup.find_all('span', {'class': "goods_pub"})
   Author_content = soup.find_all('span', {'class':'goods_auth'})
   introduction = soup.find_all('div', {'class':'goods_read'})
   add_insert = soup.find_all('div', {'class':'goods_name'})

   for i in range(len(publisher)):
      try:
         print('============================================================================')
         print(f' {num} page / {i} numder /// 진행중 >>> {itme[0].find_all("img")[i]["alt"]}')
         title_list.append(itme[0].find_all('img')[i]['alt'])
         publisher_list.append(str(publisher[i].text))
         Author_list.append(Author_content[i].text.strip())
         introduction_list.append(introduction[i].text.strip())
         str_url = str(add_insert[i].find_all('a')[1]['href'])

         if str_url.startswith('/Product/Goods'):
            url_list.append(f'http://www.yes24.com{str_url}')

            url2 = f'http://www.yes24.com{str_url}'
            # 웹 서버에 요청하기
            res2 = requests.get(url2)
            res2.raise_for_status()

            # soup 객체 만들기
            soup2 = BeautifulSoup(res2.text, "lxml")
            summery_2 = soup2.find_all('div', {'class': 'infoWrap_txtInner'})
            str_summery = summery_2[0].find_all('textarea')[0].text.strip()
            str_summery_re = str_summery.replace(',', '')
            summery_list.append(str_summery_re)
            try:
               try:
                  keyword = find_keyword(str_summery_re, n_gram_range=(3, 7))[1]
                  print('keyword >>', keyword)
                  keyword_list.append(list(keyword))
               except:
                  keyword = find_keyword(str_summery_re, n_gram_range=(2, 2))[1]
                  print('keyword >>', keyword)
                  keyword_list.append(list(keyword))
            except:
               print('keyword ERR')
               keyword_list.append(['없음'])

      except Exception as e:
         print('PASSS > ', e)
         pass

   try:
      print('파일 저장 과정')
      DF = pd.DataFrame(zip(title_list, publisher_list, Author_list, introduction_list, url_list, summery_list, keyword_list),
               columns=["title_list", "publisher_list", "Author_list_list", "introduction_list", "url_list", "summery", "keyword_list"])
      DF.to_csv('book_txt.csv', mode='a', header=False, index=False)

   except Exception as e:
      print('파일 저장 실패 PASSS > ', e)
      pass




