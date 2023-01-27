import pandas as pd



data = pd.read_csv('data_save2.csv')

data = data[['txt', 'words', 'title', 'summery', 'summery_word', 'similarity',
       'label', 'summery2', 'summery1']]

for i in range(len(data)):
    print('======================================================================')
    print(f"summery1 >> {data['summery1'].get_value(i)}")
    print(f"summery2 >> {data['summery2'].get_value(i)}")
    if data['summery1'].get_value(i) == data['summery2'].get_value(i):
        data.drop(i)
    elif data['summery2'].get_value(i) == 'CONT SUMMERY':
        data.drop(i)

data.to_csv('data_save2.csv', sep=',', index=False)

