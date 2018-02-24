
# coding: utf-8

# In[288]:


import re
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as dates
import matplotlib
get_ipython().run_line_magic('matplotlib', 'inline')
matplotlib.style.use('ggplot')
plt.rcParams['figure.figsize'] = (20.0, 10.0)


# In[289]:


pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.precision', 8)


# In[290]:


PRECISION = 8
f = "TradeHistory.xlsx"


# In[291]:


df = pd.read_excel(f)
df['Date'] = pd.to_datetime(df['Date'])
df.sort_values('Date', inplace=True)


# In[292]:


df['BuyTotal'] = float(0)
df['AmountTotal'] = float(0)
df['BTCProfit'] = float(0)
df['ETHProfit'] = float(0)


# In[293]:


df['Price'] = df['Price'].apply(lambda x: round(x,PRECISION))
df['Total'] = df['Total'].apply(lambda x: round(x,PRECISION))


# In[294]:


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


# In[295]:


df['BTCProfit'] = df['BTCProfit'].apply(lambda x: round(x,PRECISION))
df['ETHProfit'] = df['ETHProfit'].apply(lambda x: round(x,PRECISION))


# In[296]:


df['Profit'] = df.groupby(['Market'])['BTCProfit'].transform('sum')


# In[297]:


df['CProfit'] = df['BTCProfit'].cumsum()


# In[298]:


df.head(8)


# In[299]:


TotalProfit = round(df['BTCProfit'].sum(),PRECISION)
print('BTC =>', TotalProfit)
print('ETH =>', df['ETHProfit'].sum())


# In[300]:


df.set_index('Date',inplace=True)


# In[303]:


plt.style.use('dark_background')

fig, ax = plt.subplots()
ax = df['CProfit'].plot(color='b')
#set ticks every week
ax.xaxis.set_major_locator(dates.DayLocator())
#set major ticks format
ax.xaxis.set_major_formatter(dates.DateFormatter('%b %d'))
#ax.grid(color='b', linestyle='-', linewidth=0.5)
#ax.xaxis_date()
#ax.xaxis.set_major_formatter(dates.DateFormatter('%Y-%m-%d %H:%M'))
plt.xlabel('Date')
plt.ylabel('Earned')
plt.title('Total Bitcoin Earned')
#plt.legend()
plt.rc('grid', linestyle="--", color='grey', linewidth=0.25)
plt.grid(True)
plt.tight_layout()
ax.plot()

