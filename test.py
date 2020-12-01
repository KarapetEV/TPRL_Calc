import pandas as pd

def make_params_dict(df, params):
    d_2 = {}
    for row in range(df['Параметр'].shape[0]):
        for p in params:
            if df['Параметр'][row] == p[0]:
                if df['Параметр'][row] not in d_2:
                    d_2[df['Параметр'][row]] = [df['Задача'][row]]
                else:
                    d_2[df['Параметр'][row]].append(df['Задача'][row])
    return d_2


def make_level_dict(df, params):
    d_1 = {}
    for level in df['Уровень'].unique():
        if level not in d_1:
            x = [str(level)]
            d = df.loc[df['Уровень'].isin(x)]
            d_1[x[0]] = make_params_dict(d, params)
    return d_1

rad = ['S', 'B']
params = ['TRL', 'MRL', 'CRL']
data = pd.read_excel('Tasks.xlsx', index_col='Тип')
df = data.drop(rad)
val = make_level_dict(df, params)

for i, key in enumerate(val.items()):
    print(i, f'Уровень {key[0]}')
    for j, v in enumerate(key[1].items()):
        for idx in range(len(v[1])):
            print(v[0], v[1][idx])

