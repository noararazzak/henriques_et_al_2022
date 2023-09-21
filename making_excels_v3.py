import os
import pandas as pd
from pandas import ExcelWriter
import xlsxwriter

if not os.path.isdir("empty_excels"):
    os.mkdir("empty_excels")


def make_lists(file):
    output_list = []
    with open(file, 'r') as f:
        for line in f:
            output_list.append(line.split(None, 1)[0])
    return output_list


#all_real_estate = make_lists('real_estate_all.txt')
#real_estate_active = make_lists('real_estate_active.txt')
#real_estate_passive = list(set(all_real_estate) - set(real_estate_active))

#all_financials = make_lists('financials_all.txt')
#financials_active = make_lists('financials_active.txt')
#financials_passive = list(set(all_financials) - set(financials_active))

#health_active = make_lists('health_active.txt')
#health_passive = make_lists('health_passive.txt')

#industrial_active = make_lists('industrial_active.txt')
#industrial_passive = make_lists('industrial_passive.txt')

#materials_active = make_lists('materials_active.txt')
#materials_passive = make_lists('materials_passive.txt')

#technology_active = make_lists('technology_active.txt')
#technology_passive = make_lists('technology_passive.txt')

#utilities_active = make_lists('utilities_active.txt')
#utilities_passive = make_lists('utilities_passive.txt')

thematic_active = make_lists('thematic_active.txt')
thematic_passive = make_lists('thematic_passive.txt')

thematic_passive_1 = thematic_passive[:92]
thematic_passive_2 = thematic_passive[92:]

print(thematic_active)
print(thematic_passive_1)
print(thematic_passive_2)


filename_active = "empty_excels" + os.path.sep + "thematic_active_v3" + ".xlsx"

writer = pd.ExcelWriter(filename_active, engine='xlsxwriter', mode='w')
for i in thematic_active:
    df = pd.DataFrame({'Security': ['Field', 'Field', 'Field', 'Field', 'Field', 'Filed', 'Start Date', 'End Date',
                                    'Period', '', '', '', 'Security', 'Security'],
                       i + ' ' + 'US' + ' ' + 'Equity': ['PX_LAST', 'EQY_SHARPE_RATIO', 'EQY_RAW_BETA', 'EQY_ALPHA',
                                                         'FUND_INCEPT_DT', 'FUND_NET_ASSET_VAL', '',
                                                         '06/15/2022', 'per = CM', '', '', '', 'SPX Index',
                                                         'GT10 Govt'],
                       'a': ['', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                       'PX_LAST': ['', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                       'b': ['', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                       'FUND_NET_ASSET_VAL': ['', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                       'c': ['', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                       'SP_INDEX': ['', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                       'd': ['', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                       'GT10_GOVT': ['', '', '', '', '', '', '', '', '', '', '', '', '', '']})
    df.set_index('Security', inplace=True)
    df.to_excel(writer, sheet_name=i)

writer.save()

filename_passive = "empty_excels" + os.path.sep + "thematic_passive_1_v3" + ".xlsx"

writer_2 = pd.ExcelWriter(filename_passive, engine='xlsxwriter', mode='w')
for i in thematic_passive_1:
    df = pd.DataFrame({'Security': ['Field', 'Field', 'Field', 'Field', 'Field', 'Filed', 'Start Date', 'End Date',
                                    'Period', '', '', '', 'Security', 'Security'],
                       i + ' ' + 'US' + ' ' + 'Equity': ['PX_LAST', 'EQY_SHARPE_RATIO', 'EQY_RAW_BETA', 'EQY_ALPHA',
                                                         'FUND_INCEPT_DT', 'FUND_NET_ASSET_VAL', '',
                                                         '06/15/2022', 'per = CM', '', '', '', 'SPX Index',
                                                         'GT10 Govt'],
                       'a': ['', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                       'PX_LAST': ['', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                       'b': ['', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                       'FUND_NET_ASSET_VAL': ['', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                       'c': ['', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                       'SP_INDEX': ['', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                       'd': ['', '', '', '', '', '', '', '', '', '', '', '', '', ''],
                       'GT10_GOVT': ['', '', '', '', '', '', '', '', '', '', '', '', '', '']})

    df.set_index('Security', inplace=True)
    df.to_excel(writer_2, sheet_name=i)

writer_2.save()
