# -*- coding: utf-8 -*-
"""Phyton project test.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1nQPAk02Ng6FskEwP3TdnfcRY946bsxLr

# 0. Imports
"""

!pip install yfinance

import pandas as pd
from bs4 import BeautifulSoup
import requests
import yfinance as yf
from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import ipywidgets as widgets
import plotly.express as px
import plotly.graph_objects as go

"""# 1. Scrap Data from coinmarketcap.com"""

#Create empty lists to store the data
crypto_name_list = []
crypto_market_cap_list = []
crypto_price_list = []
crypto_circulating_supply_list = []
crypto_symbol_list = []
crypto_volume_list = []

#create a function to scrape data where we can select date and number of crypto
def cryptoscrape(date,n):
    """
    Scrapes the data from the coinmarketcap website 

    Parameters:  
    - date: A string specifying the date until which the database of coinmarketcap should be upadted (use today's date if you want most recent data)
    - n: The amount of cryptocurrencies that should be scraped and stored
    """
    url = 'https://coinmarketcap.com/historical/'+date+'/'
    webpage = requests.get(url)
    #Parse text from website
    soup = BeautifulSoup(webpage.text, 'html.parser')

    #get the table row element --> this is where the data is stored 
    tr = soup.find_all('tr',attrs={'class':'cmc-table-row'})
    #Count variable for the number of crypto that we want to scrape
    variable = 0
    #Loop through every row
    for row in tr:
        if variable == n:
            break;
        variable = variable + 1 #we will stop after scrapping n cryptos

        #store name of crypto
        #find the td element (Column) to get the name
        name_column = row.find('td',attrs={'class':'cmc-table__cell cmc-table__cell--sticky cmc-table__cell--sortable cmc-table__cell--left cmc-table__cell--sort-by__name'})
        crypto_name = name_column.find('a',attrs={'class':'cmc-table__column-name--name cmc-link'}).text.strip()
        crypto_name_list.append(crypto_name)
        #store symbol
        crypto_symbol = name_column.find('a', attrs={'class':'cmc-table__column-name--symbol cmc-link'}).text.strip()
        crypto_symbol_list.append(crypto_symbol)
        #store market cap
        crypto_market_cap = row.find('td', attrs={'class':'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__market-cap'}).text.strip()
        crypto_market_cap_list.append(crypto_market_cap)
        #Price
        crypto_price = row.find('td',attrs={'class':'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__price'}).text.strip()
        crypto_price_list.append(crypto_price)
        #circulating supply
        crypto_supply = row.find('td', attrs={'class':'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__circulating-supply'}).text.strip()
        crypto_supply2 = crypto_supply.split(' ',1)[0]
        crypto_circulating_supply_list.append(crypto_supply2)
        #volume
        crypto_volume = row.find('td', attrs={'class':'cmc-table__cell cmc-table__cell--sortable cmc-table__cell--right cmc-table__cell--sort-by__volume-24-h'}).text.strip()
        crypto_volume_list.append(crypto_volume)

#Get yesterday's date and convert it to the correct format to be used in our function
import datetime
yesterday = date.today()-datetime.timedelta(days=1)
#Calling our function with yesterday's date and the number of crypto wanted
cryptoscrape(yesterday.strftime("%Y%m%d"), 20)

#Create a data frame and store data
df = pd.DataFrame()
df['Name'] = crypto_name_list
df['Symbol'] = crypto_symbol_list
df['Market Cap'] = crypto_market_cap_list
df['Price'] = crypto_price_list
df['Number of Tokens circulating'] = crypto_circulating_supply_list
df['Volume last 24h'] = crypto_volume_list

"""#2. Data Cleaning


"""

#before building some visualizations, do some data cleaning because format is not adequate
#Column Market Cap is not a float
df['Market Cap'] = df['Market Cap'].str.replace('$','')
df['Market Cap'] = df['Market Cap'].str.replace(',','')
df['Market Cap'] = pd.to_numeric(df['Market Cap'])
#Column Volume last 24h is not a float
df['Volume last 24h'] = df['Volume last 24h'].str.replace('$','')
df['Volume last 24h'] = df['Volume last 24h'].str.replace(',','')
df['Volume last 24h'] = pd.to_numeric(df['Volume last 24h'])

df.style.format({"Market Cap": "{:,}","Volume last 24h": "{:,}"})

"""#3. We are now loading historical data of coins that we scrapped before"""

#We will use yahoofinance module to load historical data 
#we will create a dictionnary so we can store key = "BTC" and value = DataFrame containing historical data
d = {}
for i in crypto_symbol_list:
  d[i] = pd.DataFrame()

#we load data from yfinance module for each symbol and store it in the dataframes in the dictionnary
for s in crypto_symbol_list:
  ticker = yf.Ticker(s+"-USD")
  d[s] = (ticker.history(start = '2017-12-21', end = '2022-12-21', interval = '1d'))
  #we only keep revelant column
  d[s] = d[s][["Close"]] 
  #change format of the date
  d[s].index = pd.to_datetime(d[s].index, format='%m/%d/%Y').strftime('%Y-%m-%d') 
  #calculating daily return
  d[s]["Daily Return"] = d[s]["Close"].pct_change(1)

"""#4.Data has been scrapped/loaded we can used it to show some visualizations

"""

#Pie chart to show Market Cap
fig = px.pie(df, values ='Market Cap', names = 'Symbol', title = "Market cap ($) per coin in %")
fig.update_traces(textposition='inside', textinfo='percent+label')
fig.show()

#Bar chart showing Volume last 24h
fig2 = px.bar(df, x='Symbol',y='Volume last 24h')
fig2.update_layout(xaxis={'categoryorder': 'total descending'})
fig2.show()

#Historical chart
def show_hist(crypto):
  df = d[crypto].copy()
  df['Close'].plot(figsize=(12,7))
  plt.title('Historical Price'+' '+crypto)
  plt.ylabel("Price in $")
widgets.interact(show_hist, crypto = [i for i in d.keys()])

"""#5.Create Momentum strategy 



"""

cryptos_to_analyze=[]
for x in d.keys():
  if len(d[x]["Daily Return"])>1800:
    cryptos_to_analyze.append(x)

"""Creation of a Dataframe (df_returns) with the 10d historical returns of all cryptos containing enough data (i.e, cryptos with more than 1800 days of data)."""

dicto={}
for w in cryptos_to_analyze:
  list1=[]
  for i in range(180):
     #Advance by 10 days each time so 180 bins of 10 days returns each time.
    list1.append([d[w]["Close"].values[i*10:i*10+10]]) 
  list2=[x for x in range(1,181)]
  df=pd.DataFrame()
  for i, sublist in enumerate(list1):
    for j in range(len(sublist)):
      df[i]=sublist[j]
  df1=df
  listos=[]
  for i in range(len(df1.columns)):
    a=0
    a=(df1.iloc[-1,i])/(df1.iloc[0,i])-1
    listos.append(a)
  dicto[w]=listos
  df_returns=pd.DataFrame(data=dicto)

"""Add a score between 0-9 for the best, and worst performing crypto of the considered period"""

df_returns[["BTC Score","ETH Score","USDT Score","BNB Score","XRP Score","DOGE Score","ADA Score","TRX Score","LTC Score"]]=df_returns.apply(lambda x: pd.qcut(x, q=10, labels=False), axis=1)
df_returns.head()

"""isolation of a matrix containing only the scores from 0-9"""

df_scores=df_returns.iloc[:,9:]

"""Creation of a weight matrix. If the score of the previous week is 8 or 9 (high momentum) we will go long 50% + 50% of our portfolio for the next period in those 2 coins. If the score of the previous week is 0 or 1 (low performers), then we will go short -50% + -50% those 2 coins for the next period."""

df_weights=df_scores.copy()
df_weights.columns=df_weights.columns.str.replace('Score', ' Weight')
df_weights_copy=df_weights.copy()
for i in range(1,len(df_weights)):
  for j in range(len(df_weights.columns)):
    if df_weights_copy.iloc[i-1,j]==9:
      df_weights.iloc[i,j]=0.5
    elif df_weights_copy.iloc[i-1,j]==8:
      df_weights.iloc[i,j]=0.5
    elif df_weights_copy.iloc[i-1,j]==0:
      df_weights.iloc[i,j]=-0.5
    elif df_weights_copy.iloc[i-1,j]==1:
      df_weights.iloc[i,j]=-0.5
    else:
      df_weights.iloc[i,j]=0

"""Remove the first line of matrix of weights and returns to realize a scalar product of each line to calculate period performance later."""

df_weights_to_calculate=df_weights.iloc[1:,:]
df_returns_to_calculate=df_returns.iloc[1:,:9]

l=[]
for i in range(len(df_weights_to_calculate)):
  a=0
  for j in range(len(df_weights_to_calculate.columns)):
    a=a+df_weights_to_calculate.iloc[i,j]*df_returns_to_calculate.iloc[i,j]
  l.append(a)

tot_return=[]
a=1
for i in l:
  a=round(a*(1+i), 2)
  tot_return.append(a)
print("Our total return is: {returns} %".format(returns=(a-1)*100))

"""Here is a plot of the evolution of the portfolio, as we can see, it is quite volatile."""

sns.set(rc = {'figure.figsize':(15,8)})
sns.lineplot(x=df_returns_to_calculate.index,y=tot_return,color="orange").set(title='Total Return of Momentum') #Even though the return looks huge, important to take into account that cryptos like BNB were multiplied by 100x in that timeframe

"""# 6. Moving Averages Strategy

"""

def SMA_strat(crypto,MA):
  """
  Implementing the Moving Average Strategy

  Parameters:
  - crypto: The cryptocurrencies that should be included in the trading strategy
  - MA: The amount of days the moving average should be based on 
  """
  df=d[crypto].copy() 
  df["{number} MA".format(number=MA)]=df["Close"].rolling(MA).mean()
  df.dropna()
  # Now we shift the moving average 1 period backwards, i.e if the close of today is above the moving average of yesterday, we assign 1 (we will go long for the next day)
  df["Above"]=np.where(df["Close"]>df["{number} MA".format(number=MA)].shift(1),1,0)
  # Next we multiply the return of today by the position of yesterday to avoid look-ahead bias, i.e we went long yesterday and therefore we profit or loose by the value of today's change by yesterday's position
  df["Long Return"]=df["Above"].shift(1)*df["Daily Return"] 
  df.iloc[0,4]=0
  df["Portfolio ammount"]=np.cumprod(1+df["Long Return"])-1
  df["Long {coin}".format(coin=crypto)]=np.cumprod(1+df["Daily Return"])-1
  df[["Close","{number} MA".format(number=MA)]].plot(figsize=(12,7))
  df[["Portfolio ammount","Long {coin}".format(coin=crypto)]].plot(figsize=(12,7))

  print("The return of the strategy is : {dat} %".format(dat=df["Portfolio ammount"][-1]*100))
  print("The return of long only crypto is : {dat} %".format(dat=df["Long {coin}".format(coin=crypto)][-1]*100))

"""Here we can dynamicly change the MA and the cryptocurrency of our choice."""

widgets.interact(SMA_strat, crypto=[i for i in d.keys()],MA=[20,50,150,200])

"""We can observe by tweaking some of the results that some coins are proned for this kind of strategies wherease others do not observe a very good performance.

# 7. Moving Averages Cross-over
"""

def Ma_Cross(crypto):
  """
  Implementing the Moving Average Cross-over Strategy

  Parameters:
  - crypto: The cryptocurrencies that should be included in the trading strategy
  """
  df=d[crypto].copy() 
  df["50 SMA"]=df["Close"].rolling(50).mean()
  df["20 SMA"]=df["Close"].rolling(20).mean()
  df.dropna()
  # Important to look at the previous day for our case, to avoid bias
  df["Above"]=np.where(df["20 SMA"].shift(1)>df["50 SMA"].shift(1),1,0)
  # We multiply the return of today by the position of yesterday to avoid look-ahead bias, i.e we went long yesterday and therefore we profit or loose by the value of today's change by yesterday's position 
  df["Long Return"]=df["Above"].shift(1)*df["Daily Return"] 
  df.iloc[0,5]=0
  df["Portfolio ammount"]=np.cumprod(1+df["Long Return"])-1
  df["Long {coin}".format(coin=crypto)]=np.cumprod(1+df["Daily Return"])-1
  df["Indication"]=df["Above"].diff()
  df["Long"] = np.where(df["Indication"] == 1,df["Close"],np.NaN)
  df["Cash"] = np.where(df["Indication"] == -1,df["Close"],np.NaN)
  fig=px.line(df,x=df.index,y=df.Close)
  fig.add_trace(go.Scatter(x=df.index,y=df.Long,mode='markers',name="Entry",marker=dict(color='Green',size=10)))
  fig.add_trace(go.Scatter(x=df.index,y=df.Cash,mode='markers',name="Exit",marker=dict(color='Red',size=10)))
  fig.add_trace(go.Scatter(x=df.index,y=df["20 SMA"],mode='lines',name="20 SMA",marker=dict(color='Orange'),opacity=0.5))
  fig.add_trace(go.Scatter(x=df.index,y=df["50 SMA"],mode='lines',name="50 SMA", marker=dict(color='Grey'),opacity=0.5))

  fig.show()
  print("The return of the strategy is : {dat} %".format(dat=df["Portfolio ammount"][-1]*100))
  print("The return of long only crypto is : {dat} %".format(dat=df["Long {coin}".format(coin=crypto)][-1]*100))

"""Here we call the function"""

Ma_Cross("BTC")