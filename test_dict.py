# -*- coding: utf-8 -*-

import pandas as pd


def make_dict_2(data, x, params):
    dict_params = {}
    for row in range(data['Level'].shape[0]):
        if data['Level'][row] == x:
            for p in params:
                if data['Parameter'][row] == p:
                    if data['Parameter'][row] not in dict_params:
                        dict_params[data['Parameter'][row]] = [data['Pars_Name'][row], [data['Task'][row],
                                                               data['Task_Comments'][row]]]
                    else:
                        dict_params[data['Parameter'][row]].append([data['Task'][row], data['Task_Comments'][row]])
    return dict_params


def make_dict_1(data, params):
    dict_levels = {}
    for row in range(data['Level'].shape[0]):
        if data['Level'][row] not in dict_levels:
            x = data['Level'][row]
            dict_levels[x] = [data['Level_Name'][row], data['Level_Comments'][row], make_dict_2(data, x, params)]
    return dict_levels


project_type = input('Введите тип проекта: H, S, B ')
params = ['TRL', 'MRL', 'ERL', 'ORL', 'CRL']
data = pd.read_excel('Test_Tasks.xlsx', sheet_name=project_type)
levels = make_dict_1(data, params)
# print(levels)
for key, values in levels.items():
    print(key, values[0]) # values[1] комментарий к values[0]
    for k, v in values[2].items():
        print(k, v[0])
        for iter_v in v[1:]:
            print(iter_v[0]) # iter_v[1] комментарий к iter_v[0]




