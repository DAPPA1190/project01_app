#!/usr/bin/env python
# coding: utf-8

# In[1]:


##project01

#5:Streamlit 投資組合儀表板原型開發

#Step 5.1: imstall
# !pip install streamlit yfinance plotly pandas
# ↑install後記得註解掉，app會報錯(notebook專用語法)


# In[9]:


#Step 5.2: import
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

#Step 5.3: 建立 Streamlit 主程式 app.py
import streamlit as st
import yfinance as yf
import json
import numpy as np
import pandas as pd

from performance import annualized_return, annualized_volatility, sharpe_ratio, max_drawdown, calculate_portfolio_return

st.title("📈 ETF 策略分析平台")

# 原本功能：輸入單一 ETF 代碼
ticker = st.text_input("輸入 ETF 代碼，例如 VTI", "")
if ticker:
    data = yf.download(ticker, period="1y", auto_adjust=False)
    if data.empty:
        st.error("下載資料失敗，請確認代碼是否正確")
    else:
        st.line_chart(data['Adj Close'])

# 新功能：載入策略設定並使用 performance.py 計算組合績效
st.header("📊 策略組合績效分析")

# 載入策略設定
with open("portfolio_config.json", "r") as f:
    portfolio_configs = json.load(f)

strategy = st.selectbox("選擇策略", list(portfolio_configs.keys()))
weights = portfolio_configs[strategy]
tickers = list(weights.keys())

if st.button("執行策略分析"):
    data = yf.download(tickers, period="1y", auto_adjust=True)["Adj Close"].dropna()
    returns_df = np.log(data / data.shift(1)).dropna()
    portfolio_returns = calculate_portfolio_return(returns_df, weights)
    cumulative_returns = (1 + portfolio_returns).cumprod()

    ar = annualized_return(portfolio_returns)
    vol = annualized_volatility(portfolio_returns)
    sharpe = sharpe_ratio(portfolio_returns)
    mdd = max_drawdown(cumulative_returns)

    st.subheader("組合每日報酬率")
    st.line_chart(portfolio_returns)

    st.subheader("組合累積報酬率")
    st.line_chart(cumulative_returns)

    st.subheader("策略績效指標")
    st.write(f"年化報酬率：{ar:.2%}")
    st.write(f"年化波動度：{vol:.2%}")
    st.write(f"Sharpe Ratio：{sharpe:.2f}")
    st.write(f"最大回撤：{mdd:.2%}")



# In[ ]:




