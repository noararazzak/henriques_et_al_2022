import os
import pandas as pd

if not os.path.isdir("empty_excels"):
    os.mkdir("empty_excels")


def make_lists(file):
    output_list = []
    with open(file, 'r') as f:
        for line in f:
            output_list.append(line.split(None, 1)[0])
    return output_list


henriques_et_al_2022 = make_lists('henriques et al_2022_energy.txt')
print(henriques_et_al_2022)

filename_active = "empty_excels" + os.path.sep + "Henriques et al_2022_Inception" + ".xlsx"

writer = pd.ExcelWriter(filename_active, engine='xlsxwriter', mode='w')

df = pd.DataFrame(columns=('Ticker', 'Date'))

for i in henriques_et_al_2022:
    df.loc[i] = [i + ' ' + 'US' + ' ' + 'Equity', '=BDP(' + i + ',' + 'FUND_INCEPT_DT)']

df.set_index('Ticker', inplace=True)
df.to_excel(writer, sheet_name='Inception Dates')

writer.save()
