#!/usr/bin/python

import re
import pandas as pd
import datetime as dt

pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.precision', 8)

PRECISION = 8
f = "TradeHistory.xlsx"

df = pd.read_excel(f)
df['Date'] = pd.to_datetime(df['Date'])
df.sort_values('Date', inplace=True)

df['BuyTotal'] = float(0)
df['AmountTotal'] = float(0)
df['BTCProfit'] = float(0)
df['ETHProfit'] = float(0)

df['Price'] = df['Price'].apply(lambda x: round(x,PRECISION))
df['Total'] = df['Total'].apply(lambda x: round(x,PRECISION))

for k, g in df.groupby(['Market']):
    p=None
    for i, r in g.iterrows():
        if r.Type == 'BUY':
            buyTotal = round(r.Price,PRECISION) * round(r.Amount,PRECISION)
            if p is None:
                df.at[i,'BuyTotal'] = round(buyTotal,PRECISION)
            else:
                df.at[i,'BuyTotal'] = df.at[p, 'BuyTotal'] + round(buyTotal, PRECISION)

            if p is None:
                df.at[i,'AmountTotal'] = round(r.Amount,PRECISION)
            else:
                df.at[i,'AmountTotal'] = df.at[p, 'AmountTotal'] + round(r.Amount, PRECISION)
#            print(g)
        elif r.Type == 'SELL':
            if k == 'ETHBTC':
                df.at[i,'BTCProfit'] = round(r.Total,PRECISION)
                continue
            if re.search('ETH$', r.Market):
                df.at[i,'ETHProfit'] = round(r.Total,PRECISION)
            elif re.search('BTC$', r.Market):
                sellTotal = round(r.Price,PRECISION) * round(r.Amount,PRECISION)
                buyTotal = df.at[p, 'BuyTotal']
                amountTotal = df.at[p, 'AmountTotal']
                newAmount = round(amountTotal,PRECISION) - round(r.Amount,PRECISION)
                if newAmount > 0:
                    df.at[i,'AmountTotal'] = round(newAmount,PRECISION)
                else:
                    df.at[i,'AmountTotal'] = float(0)


                Profit = round(sellTotal,PRECISION) - round(buyTotal,PRECISION)
                df.at[i,'BTCProfit'] = round(Profit,PRECISION)

        else:
            continue
        p=i

df['BTCProfit'] = df['BTCProfit'].apply(lambda x: round(x,PRECISION))
df['ETHProfit'] = df['ETHProfit'].apply(lambda x: round(x,PRECISION))
df.set_index('Date', inplace=True)

print(df)

TotalProfit = round(df['BTCProfit'].sum(),PRECISION)
print('BTC =>', TotalProfit)
print('ETH =>', df['ETHProfit'].sum())

