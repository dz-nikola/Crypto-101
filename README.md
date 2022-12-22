# Crypto-101

Welcome to Crypto 101! In this project, our goal is to introduce you to the exciting world of cryptocurrencies and provide you with the tools and knowledge you need to get started in the world of crypto trading. What are the biggest cryptos? How their prices fluctuate? Is there a good trading strategy? These questions will be answered in this project.

Whether you are a complete beginner or have some familiarity with crypto, we believe that Crypto 101 has something to offer for everyone. So grab your virtual notebook and let's dive in!

*This project is part of the course "Skills: Programming - advance level" by Mario Silic at the University of St. Gallen.*

## Table of contents

## General Information

For our project we wanted to create an all-in-one place where the user can discover a few things about cryptocurrencies. 

We will first display some interesting numbers and chart about the top 20 cryptos by using data that will be scrapped from [Coinmarketcap](https://coinmarketcap.com/)

Cryptocurrencies, such as Bitcoin and Ethereum, have gained significant attention in recent years due to their potential as an alternative asset class and their use in decentralized finance (DeFi) applications. With their increasing popularity in the last couple of years, cryptocurrencies have provided investors with very profitable returns (but also very volatile!). In order to understand a bit more about those strategies, we will use 3 strategies:
* `Momentum`
* `Moving Averages`
* `Moving Averages Cross-Over`

## Technologies
* You can open the file in any IDE ??????
* Libraries used: `pandas`, `BeautifulSoup`, `requests`, `yfinance`, `date`, `matplotlib.pyplot`, `numpy`, `ipywidgets`

If a library is not installed by default, the following command needs to be run:
```
!pip install "Library name"
```

## Program Structure
### Chapter 1: Web scraping
We recommend to use the package `BeautifulSoup` to scrap the data from the website. By identifying the structure of the url, we can create a function that will scrap data from selected date. In our case we will scrap data from the day before.

### Chapter 2: Load historical data
In the last step, we loaded general data about the top 20 cryptocurrencies such as Name, Symbol, Market Capitalisation, Price and Volume in the last 24h.
In the following step we will load historical data of these cryptos using the package `yfinance` 

### Chapter 3: Data Visualization
This part will give the user an overview of the data that we just loaded by creating:
* A pie chart to show the biggest actors of the crypto environment 
* A bar chart to show the most traded coins in the last 24h
* A line chart to show the historical prices of the coins

*The Visualizations can be found here:*

### Chapter 4: Momentum Strategy
There is a common saying in the stock markets that indicates that stocks that went high, tend to go higher for a while. This is called momentum. As buyer pile in to make sure to profit from the uptrend, the price of a stock (in our case cryptocurrency) will tend to keep rising for a bit. Below we will construct a long short porfolio that takes into account the rank of each crypto-currency in the last 10 days and will decide to go long or short for the following 10 day period if the crypto was ranked approprietly. 

In other words, we will compare the performance of our coins in the last 10 days. We will buy (long position) the two best performers and sell (short position) the two worst performers. In mathematical terms:

```
Portfolio Weights = 0.5 x Top1 coin + 0.5 x Top2 coin - 0.5 x Worst1 coin - 0.5 x Worst2 coin
```

We will keep the position for a period of 10 days. After that we will look at the performance and rank once again the performance of the coins and reallocate the portfolio weights.

**What would have happenned if we had invested 1$ on December 21st 2017 and implementated this strategy until now ?**

SHOW GRAPH HERE

Our 1$ investment returned 16$ which is a 74% annualized return! This looks like an incredible startegy but let's be a little bit critical about that:

* Volatility is extremely high in this asset class, thus a coin can gain/lose more than 30% of its value in a 10-day period. 
* You can be lucky and have a long position in a coin that will skyrocket +30% in the next periods or choose a coin that will have a very poor performance.
* Important to take into account that during this timeframe some coins like BNB multiplied its value by 100 times. Thus investing in individual coin would have been more profitable

In conclusion, we don't have strong evidence that this strategy really works or if it is pure luck. Therefore we will look at the next strategy

### Chapter 5: Moving Averages strategy

As seen previously, momentum yields some result but it is hard to say if the strategy is really outperforming individual coins. Moreover, as USDT (a stable coin) was included in our dataset, it might have acted as a "safe haven" during crypto crashes. We therefore want to display another strategy that might be profitable against individual coins.

To do that, we have seen that first of all cryptos were really cylcical and that long period of outperformance could be followed by very long period of negative returns.

In order to profit from trending periods and to stay out of turbulent times, we have designed different strategies based on moving averages were the user can choose his/hers favorite crypto as well as a moving average and can see the result of the strategy in a simple graph.

The Moving average strategy works as follow:

We will compare the close value of a coin to its moving average (20 to 200 days moving average)
* If Close > MA : We are long
* If Close < MA : We sell our position and we stay out as long as Close < MA

The user will be able to select a crypto and the parameter of the moving average and compare this strategy with a long-only strategy on the coin.

### Chapter 6: Moving Averages Cross-Over
Let's look at a last strategy called the Moving Average Cross-Over

For this part we want to analyze if we can profit from a strategy where we go long the selected cryptocurrency when the fast moving average (20 SMA) is above the slower moving average (50 SMA). The rationale behind this strategy is that when the faster moving average is above the slower one, we can conclude that there is a confirmed uptrend from which we can profit. When the faster moving average is below the slower one, it might indicates the beginning of a downtrend where we do not want to hold a position.
