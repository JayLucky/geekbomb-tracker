
# coding: utf-8

# In[265]:


import re
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt


# In[266]:


pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.precision', 8)


# In[267]:


PRECISION = 8
f = "TradeHistory.xlsx"


# In[268]:


df = pd.read_excel(f)
df['Date'] = pd.to_datetime(df['Date'])
df.sort_values('Date', inplace=True)
df.set_index('Date',inplace=True)


# In[269]:


df['Price'] = df['Price'].apply(lambda x: round(x,PRECISION))
df['Total'] = df['Total'].apply(lambda x: round(x,PRECISION))


# In[270]:


df.head()


# In[271]:


def fa(r):
    if r[1] == 'BUY':
        return np.negative(r[3])
    else:
        return r[3]


# In[272]:


df['NewAmount'] = df.apply(fa, axis=1)


# In[273]:


def ft(r):
    if r[1] == 'BUY':
        return np.negative(r[4])
    else:
        return r[4]


# In[274]:


df['NewTotal'] = df.apply(ft, axis=1)


# In[367]:


df['Profit'] = df.groupby(['Market'])['NewTotal'].transform('sum')


# In[369]:


df


# In[359]:


plt.figure(figsize=(20,10))
g.plot()


# In[ ]:




