import os
import pandas as pd
import json
from find_keyword import *



num = 0

file_path1 = 'D:/AIhub/도서자료 요약'
file_list = os.listdir(file_path1)
for i in file_list:
    file_path2 = file_path1 + f'/{i}'
    file_list2 = os.listdir(file_path2)
    for j in file_list2:
        file_path3 = file_path2 + f'/{j}'
        file_list3 = os.listdir(file_path3)
        for ij in file_list3:
            file_path4 = file_path3 + f'/{ij}'

            num += 1
            file_path_data = file_path4

            if num < 5491:
                continue

            print(f'=== {num} ===========================================================')
            print(f'진행중 {file_path_data} ')

            try:
                with open(file_path_data, 'rt', encoding='UTF-8') as json_file:
                    json_data = json.load(json_file)
                    metadata = json_data['metadata']
                    doc_name = metadata.get('doc_name')
                    kdc_label = metadata.get('kdc_label')
                    publisher = metadata.get('publisher')
                    author = metadata.get('author')
                    passage = json_data.get('passage')
                    summary = json_data.get('summary')
                    passage_keyword = find_keyword(passage)
                    summary_keyword = find_keyword(summary)

                    # print('doc_name   >>>>>', doc_name)
                    # print('kdc_label  >>>>>', kdc_label)
                    # print('publisher  >>>>>', publisher)
                    # print('passage    >>>>>', passage)
                    # print('summary    >>>>>', summary)
                    # print('passage_keyword >>>>> ', passage_keyword[1])
                    # print('summary_keyword >>>>> ', summary_keyword[1])

                    data_dic = {'title': str(j),
                                'doc_name': doc_name,
                                'author': author,
                                'kdc_label': kdc_label,
                                'publisher': publisher,
                                'passage': passage,
                                'summary': summary,
                                'passage_keyword': passage_keyword[1],
                                'summary_keyword': summary_keyword[1]}

                    print('data_dic : \n', data_dic)

                    df = pd.DataFrame.from_dict(data=data_dic, orient='columns')
                    df.to_csv('output.csv', index=False, mode='a', encoding='utf-8-sig', header=False)
            except Exception as e:
                print('e >>>', e)

            json_file.close()