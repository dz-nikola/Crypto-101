# Crypto-101

Welcome to Crypto 101! Our goal is to introduce you to the exciting world of cryptocurrencies and give you the tools and knowledge you need to get started in the craft of crypto trading. What are the major cryptocurrencies? How do their prices fluctuate? Is there a good trading strategy? These are the questions that will be answered in this project.

Whether you are a complete beginner or already know a bit about cryptocurrencies, we believe that Crypto 101 has something to offer for everyone. So grab your virtual notebook and let's dive in!

*This project is part of the course "Skills: Programming - advance level" by Mario Silic at the University of St. Gallen.*

## Table of contents
- [General Information](#general-information)
- [Technologies](#technologies)
- [Program Structure](#program-structure)
  - [1 - Web Scraping](#1---web-scraping)
  - [2 - Load historical data](#2---load-historical-data)
  - [3 - Data Visualization](#3---data-visualization)
- [Trading Strategies](#trading-strategies)
  - [Strategy 1 - Momentum Strategy](#strategy-1---momentum-strategy)
  - [Strategy 2 - Moving Averages](#strategy-2---moving-averages)
  - [Strategy 3 - Moving Averages Cross-Over](#strategy-3---moving-averages-cross-over)
- [Authors](#authors)
- [Code](#code)

## General Information

For our project, we wanted to create an all-in-one place where users can discover for themselves a few things about cryptocurrencies. 

We will first show some interesting numbers and charts about the top 20 cryptocurrencies by using data that comes from [Coinmarketcap](https://coinmarketcap.com/).

In recent years, cryptocurrencies such as Bitcoin and Ethereum have attracted significant attention due to their potential as an alternative asset class and their use in decentralized financial applications (DeFi). With their increasing popularity in recent years, cryptocurrencies have provided investors with very lucrative returns (but also very volatile!). To learn a little more about these trading strategies, we will cover 3 of them:
* `Momentum`
* `Moving Averages`
* `Moving Averages Cross-Over`

## Technologies
* We used Google Colab to run the notebook. We highly recommend our users to run the code on Google Colab as well. Please find the link to our Code below.
* Libraries used: `pandas`, `BeautifulSoup`, `requests`, `yfinance`, `date`, `matplotlib.pyplot`, `numpy`, `ipywidgets`, `plotly`

If a library is not installed by default, the following command needs to be run:
```
!pip install "Library name"
```

## Program Structure
### 1 - Web Scraping
We recommend using the `BeautifulSoup` package to retrieve the data from the website. By identifying the structure of the URL, we can create a function that fetches data from a specific date. In our case, we will scrape the data from the previous day.

### 2 - Load historical data
As a final step, we have loaded general data about the top 20 cryptocurrencies, such as name, symbol, market capitalization, price and volume in the last 24 hours.
The following stage is where we will load historical data of these cryptocurrencies using the "yfinance" package 

### 3 - Data Visualization
This part will give the user an overview of the data that we just loaded by creating:
* A pie chart to show the biggest actors of the crypto environment 
* A bar chart to show the most traded coins in the last 24h
* A line chart to show the historical prices of the coins

Having shown the basics of the crypto environment, we will now turn our focus to developing trading strategies for maximizing returns in this exciting and dynamic market.

## Trading Strategies

**Disclaimer**: Our trading strategies did not consider the timing of trades. However, timing is a crucial factor in realizing returns, as it can have a significant impact on the success or failure of a trade. It is important to consider timing when evaluating the effectiveness of our trading strategies, as it can play a major role in determining their success or failure. The big discrepance between the the return of our moving-average cross-over strategy can be explained by the good timing as well as by profiting from getting out before the happening of the huge crypto crash in 2022. Lastly, the trading costs were not considered.

### Strategy 1 - Momentum Strategy
There is a common saying in the stock markets that indicates that stocks that went high, tend to go higher for a while. This is called momentum. As buyer pile in to make sure to profit from the uptrend, the price of a stock (in our case cryptocurrency) will tend to keep rising for a bit. Below we will construct a long short porfolio that takes into account the rank of each crypto-currency in the last 10 days and will decide to go long or short for the following 10-day period if the crypto was ranked approprietly. 

In other words, we will compare the performance of our coins in the last 10 days. We will buy (long position) the two best performers and sell (short position) the two worst performers. In mathematical terms:

```
Portfolio Weights = 0.5 x Top1 coin + 0.5 x Top2 coin - 0.5 x Worst1 coin - 0.5 x Worst2 coin
```

We will keep the position for a period of 10 days. After that we will look at the performance and rank once again the performance of the coins and reallocate the portfolio weights.

**What would have happenned if we had invested 1$ on December 21st 2017 and implementated this strategy until now ?**

[Click here to see portfolio amount](Portfolio_amount_momentum.png)

Our 1$ investment returned 16$ which is a 74% annualized return! This looks like an incredible startegy but let's be a little bit critical about that:

* Volatility is extremely high in this asset class, thus a coin can gain/lose more than 30% of its value in a 10-day period. 
* You can be lucky and have a long position in a coin that will skyrocket +30% in the next periods or choose a coin that will have a very poor performance.
* Important to take into account that during this timeframe some coins like BNB multiplied its value by 100 times. Thus investing in individual coin would have been more profitable

In conclusion, we don't have strong evidence that this strategy really works or if it is pure luck. Therefore we will look at the next strategy

### Strategy 2 - Moving Averages

As seen previously, momentum yields some results but it is hard to say if the strategy is really outperforming individual coins. Moreover, as USDT (a stable coin) was included in our dataset, it might have acted as a "safe haven" during crypto crashes. We therefore want to display another strategy that might be profitable against individual coins.

To do that, we have seen that first of all cryptos were really cylcical and that long period of outperformance could be followed by very long period of negative returns.

In order to profit from trending periods and to stay out of turbulent times, we have designed different strategies based on moving averages were the user can choose his/her favorite crypto as well as a moving average and can see the result of the strategy in a simple graph.

The Moving average strategy works as follows:

We will compare the close value of a coin to its moving average (20 to 200 days moving average)
* If Close > MA : We are long
* If Close < MA : We sell our position and we stay out as long as Close < MA

The user will be able to select a crypto and the parameter of the moving average and compare this strategy with a long-only strategy on the coin.

### Strategy 3 - Moving Averages Cross-Over
Let's look at a last strategy called the Moving Average Cross-Over

For this part we want to analyze if we can profit from a strategy where we go long the selected cryptocurrency when the fast moving average (20 SMA) is above the slower moving average (50 SMA). The rationale behind this strategy is that when the faster moving average is above the slower one, we can conclude that there is a confirmed uptrend from which we can profit. When the faster moving average is below the slower one, it might indicates the beginning of a downtrend where we do not want to hold a position.

## Authors
Loïc Mathys

Nikola Golubovic

Noah Nolè

## Code
Link to our Google Colab with the code and comments included:

https://colab.research.google.com/drive/1nQPAk02Ng6FskEwP3TdnfcRY946bsxLr?usp=sharing#scrollTo=dIsGTYp0YoVW 
