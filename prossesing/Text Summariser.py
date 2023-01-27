from gensim.summarization.summarizer import summarize
import pandas as pd
import re, random


Org_data = pd.read_csv("data_save.csv")
summery = Org_data['summery']

summery1 = []
summery2_list = []
for index, txt in enumerate(summery):
    # text = re.compile('[가-힣]+').search(txt)
    text = re.sub('\n', ' ', txt)
    summery1.append(text)
    print('\n ========================================================================================================')
    print('index >>', index)
    print('text  >>', text)
    try:
        summery2 = ''
        R_num_count = 0
        while True:
            if R_num_count > 60:
                raise Exception
            if len(str(summery2)) == 0:
                R_num_count += 1
                R_num = random.randrange(10, 35)
                summery2 = summarize(str(text), word_count=R_num)
            elif len(str(summery2)) != 0:
                print('summery2 >>', summery2)
                summery2 = re.sub('\n', ' ', summery2)
                summery2_list.append(summery2)
                break

    except Exception as e:
        summery2 = 'CONT SUMMERY'
        summery2_list.append(summery2)
        print('ERR !!!!!!')
        print( e)


Org_data['summery2'] = summery2_list
Org_data['summery1'] = summery1

Org_data.to_csv('data_save2.csv', sep=',', index=False)

