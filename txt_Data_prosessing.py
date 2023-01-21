import pandas as pd
import json
import os


json_path = 'C:/Users/HERO/Downloads/sample/06.edit/20per'
path = os.listdir(json_path)


answer_list = []

for i in path:
    path_data = json_path + '/' + i

    with open(path_data, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

        summary = json_data['Annotation']['summary1']
        answer_list.append(str(summary))










