#!/usr/bin/env python
# coding: utf-8

# In[1]:


##project01
#2:計算個別資產日報酬率：

#Step 2.1: import
#!pip install yfinance
# ↑install後記得註解掉，app會報錯(notebook專用語法)

import yfinance as yf
import pandas as pd
import json
import os
import numpy as np
import matplotlib.pyplot as plt

#Step 2.2: 載入 portfolio_config.json
with open("config/portfolio_config.json", "r") as f:
    portfolio_config = json.load(f)

#Step 2.3: strategy choice
strategy_name = "custom"
weights = portfolio_config[strategy_name]
tickers = list(weights.keys())

#Step 2.4: 載入歷史價格資料（from merged CSV Files）
def load_price_data(tickers, data_folder="Adj close"):
    price_df = pd.DataFrame()
    for ticker in tickers:
        file_path = os.path.join(data_folder, f"{ticker}.csv")
        try:
            df = pd.read_csv(file_path, index_col=0, parse_dates=True)
            price_df[ticker] = df["Adj Close"]
        except Exception as e:
            print(f"⚠ 無法讀取 {ticker}.csv：{e}")
    return price_df

price_df = load_price_data(tickers)

#Step 2.5: 日報酬率可視化
returns_df = np.log(price_df / price_df.shift(1)).dropna()
for ticker in returns_df.columns:
    plt.figure(figsize=(10, 4))
    plt.plot(returns_df.index, returns_df[ticker], label=ticker)
    plt.title(f"daily - {ticker} (Log Return)")
    plt.ylabel("Daily Return")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


# In[3]:


#3.計算投資組合整體報酬

#Step 3.1: 根據 portfolio_config 中的權重進行加權
def calculate_portfolio_return(returns_df, weights_dict):
    weights = np.array([weights_dict[ticker] for ticker in returns_df.columns])
    return returns_df.dot(weights)

portfolio_returns = calculate_portfolio_return(returns_df, weights)

#Step 3.2: 畫出投資組合每日加權報酬折線圖
plt.figure(figsize=(10, 4))
plt.plot(portfolio_returns.index, portfolio_returns, label="Portfolio Daily Return")
plt.title(f"daily raturn - {strategy_name}")
plt.ylabel("Daily Return")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()


# In[4]:


#4:績效計算與可視化

#Step 4.1: 績效指標函數
#年化報酬率
def annualized_return(r):
    return np.mean(r) * 252

#年化波動度
def annualized_volatility(r):
    return np.std(r) * np.sqrt(252)

#Sharpe Ratio
def sharpe_ratio(r, rf=0.0):
    excess = r - rf / 252
    return annualized_return(excess) / annualized_volatility(r)

#最大回撤
def max_drawdown(cumulative):
    peak = cumulative.cummax()
    drawdown = cumulative / peak - 1
    return drawdown.min()


# Step 4.2: 績效指標計算
cumulative_returns = (1 + portfolio_returns).cumprod()
ar = annualized_return(portfolio_returns)
vol = annualized_volatility(portfolio_returns)
sharpe = sharpe_ratio(portfolio_returns)
mdd = max_drawdown(cumulative_returns)


# Step 4.3: 績效指標可視化
print("--- 策略績效 ---")
print(f"策略名稱：{strategy_name}")
print(f"年化報酬率：{ar:.2%}")
print(f"年化波動度：{vol:.2%}")
print(f"Sharpe Ratio：{sharpe:.2f}")
print(f"最大回撤：{mdd:.2%}")
plt.figure(figsize=(10, 5))
plt.plot(cumulative_returns, label=strategy_name)
plt.title("Portfolio Cumulative Return")
plt.ylabel("Cumulative Return")
plt.grid(True)
plt.legend()
plt.show()







