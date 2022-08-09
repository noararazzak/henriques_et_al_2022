import os
import pandas as pd
from scipy import stats
import math
import logging
from pandas.tseries.offsets import MonthEnd
import datetime

directory = 'C:/Users/Noara/OneDrive/Summer 2022/Data/csv_cleaned/henriques_et_al'

#directory = os.fsencode(directory_in_str)
min_number = 1
days = 365
months = 12
number_trading = 252
year = [2014, 2015, 2016, 2017, 2018]


class Property():
    def __init__(self, ticker, beta, std_dev, sharpe, jensen_alpha, total_trailing_return, mean_annual_return):
        self.ticker = ticker
        self.beta = beta
        self.std_dev = std_dev
        self.sharpe = sharpe
        self.jensen_alpha = jensen_alpha
        self.total_trailing_return = total_trailing_return
        self.mean_annual_return = mean_annual_return


all_csv_property = []


def slice_by_date(data, year):
    data = data[data.index.year.isin(year)]
    return data


def get_return_of_asset(data, field):
    data = data[field].pct_change()
    data = data * 100
    return data


def get_risk_free_rate(element):
    answer = (element / 100) + 1
    answer = answer ** (1 / months)
    answer = (answer - 1) * 100
    return answer


def get_annualized_return_2(field, n):
    answer = stats.gmean(df.loc[:, field])
    power = number_trading / n
    answer = answer ** power
    answer = answer - 1
    return answer


def get_annualized_return(data, field):
    total = 0
    for entry in data[field]:
        total = total + entry

    return total


def get_annualized_risk(data, field):
    answer = data[field].std()
    answer = answer * math.sqrt(months)
    return answer


def mean_annual_return(data, field):
    annualreturn_list = []
    for yr in year:
        value = data.loc[data['Year'] == yr, field].sum()
        annualreturn_list.append(value)
        answer = sum(annualreturn_list) / len(annualreturn_list)
    return answer, annualreturn_list


def get_first_value_column(data, field):
    answer = data.loc[data.index[0], field]
    return answer


def get_last_value_column(data, field):
    answer = data.loc[data.index[-1], field]
    return answer


def get_beta(data, field_1, field_2):
    answer = stats.linregress(data[field_1], data[field_2]).slope
    return answer


def get_alpha(data, field_1, field_2):
    answer = stats.linregress(data[field_1], data[field_2]).intercept
    return answer


for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".csv"):
        csv_path = os.path.join(directory, filename)
        print(csv_path)
        df = pd.read_csv(csv_path, index_col=False)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.groupby([df['Date'].dt.year, df['Date'].dt.month], as_index=False).last()
        df['Year'] = pd.DatetimeIndex(df['Date']).year
        df.set_index('Date', inplace=True)
        if (len(df)) >= min_number:
            ticker_csv = filename.split(None, 1)[0]
            df = slice_by_date(df, year)
            n = len(df)
            print(df)
            df['PX_LAST_RATE'] = get_return_of_asset(df, 'PX_LAST')
            df['MT_INDEX_RATE'] = get_return_of_asset(df, 'MT_INDEX')
            annualized_risk_free = get_first_value_column(df, 'GT10_GOVT')
            net_present_in = get_first_value_column(df, 'FUND_NET_ASSET_VAL')
            net_present_f = get_last_value_column(df, 'FUND_NET_ASSET_VAL')
            df = df.iloc[1:, :]
            annualized_return_s = get_annualized_return(df, 'PX_LAST_RATE')
            annualized_return_b = get_annualized_return(df, 'MT_INDEX_RATE')
            df['RISK_FREE_D'] = df[['GT10_GOVT']].apply(get_risk_free_rate)
            df['EXCESS_PX_LAST'] = df['PX_LAST_RATE'] - df['RISK_FREE_D']
            df['EXCESS_MT_INDEX'] = df['MT_INDEX_RATE'] - df['RISK_FREE_D']
            beta_csv = get_beta(df, 'EXCESS_MT_INDEX', 'EXCESS_PX_LAST')
            std_csv = get_annualized_risk(df, 'PX_LAST_RATE')
            sharpe_csv = (annualized_return_s - annualized_risk_free) / std_csv
            jensen_csv = annualized_return_s - (annualized_risk_free + beta_csv * (annualized_return_b -
                                                                                   annualized_risk_free))
            trailing_csv = ((net_present_f - net_present_in) / net_present_in) * 100
            mean_annual_csv, mean_annual_list = mean_annual_return(df, 'PX_LAST_RATE')
            print(annualized_risk_free, annualized_return_s, annualized_return_b)
            logging.basicConfig(filename='dataset.log', encoding='utf-8', level=logging.DEBUG, filemode="w")
            logging.info(df.to_string())
            current_csv_prop = Property(ticker_csv, beta_csv, std_csv, sharpe_csv, jensen_csv, trailing_csv,
                                        mean_annual_csv)
            all_csv_property.append(current_csv_prop)
        continue
    else:
        continue

df_final = pd.DataFrame([{'Ticker': s.ticker, 'Beta': s.beta, 'Std Dev': s.std_dev, 'Sharpe': s.sharpe,
                          'Jensen': s.jensen_alpha, 'Trailing': s.total_trailing_return, 'Annual': s.mean_annual_return}
                         for s in all_csv_property])

print(df_final)
