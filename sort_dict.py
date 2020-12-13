import pandas as pd

def make_levels_dict(data):
    dict_levels = {}
    for rank in range(data['Уровень'].shape[0]):
        dict_levels[data['Уровень'][rank]] = [data['TPRL'][rank], data['TRL'][rank], data['MRL'][rank],
                             data['ERL'][rank], data['ORL'][rank], data['CRL'][rank]]
    return dict_levels


op_data = pd.read_excel('Levels.xlsx')
levels = make_levels_dict(op_data)
print(levels)
x =int(input('Enter TPRL level'))
for key, values in levels.items():
    if key == x:
        for v in values:
            print(f'{v}')


