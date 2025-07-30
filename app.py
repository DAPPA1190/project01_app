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
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Step 5.3: 建立 Streamlit 主程式 app.py (單一ETF 查詢)
# performance.py績效函數
from performance import annualized_return, annualized_volatility, sharpe_ratio, max_drawdown, calculate_portfolio_return

# 單一ETF查詢
st.title("📈 單一ETF 查詢")
ticker = st.text_input("輸入 ETF 代碼，例如 VTI", "")

# 日期選擇(key=date1，和組合分析區隔)
START_DATE = st.date_input("開始日期(2016起):", value=pd.to_datetime("2020-01-01"), key="START_DATE1")
END_DATE = st.date_input("結束日期:", value=pd.to_datetime("2024-12-31"), key="END_DATE1")

# main
if ticker:
    data = yf.download(ticker, start=START_DATE, end=END_DATE, auto_adjust=False)["Adj Close"]
    if data.empty:
        st.error("下載資料失敗，請確認代碼是否正確")
    else:
        st.line_chart(data)



# In[ ]:


# Step 5.4: 建立 Streamlit 主程式 app.py (組合績效查詢)
st.header("📊 策略組合績效分析")

# 從portfolio_config.json載入策略設定
with open("config/portfolio_config.json", "r") as f:
    portfolio_configs = json.load(f)
strategy = st.selectbox("選擇預設策略或上傳csv自訂組合", list(portfolio_configs.keys()))

# 若選擇custom，開啟上傳功能並覆蓋原portfolio_config檔的custom預設組合
if strategy == "custom":
    uploaded_file = st.file_uploader("請上傳自訂投資組合 CSV（格式：Ticker,Weight）", type=["csv"])
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            if "Ticker" not in df.columns or "Weight" not in df.columns:
                st.error("❌ 格式錯誤，請包含 'Ticker' 與 'Weight' 欄位")
            else:
                total_weight = df["Weight"].sum()
                if abs(total_weight - 1.0) > 0.01:
                    st.warning(f"⚠️ 權重加總為 {total_weight:.4f}，應接近 1")
                else:
                    custom_configs = dict(zip(df["Ticker"], df["Weight"]))
                    portfolio_configs["custom"] = custom_configs  
                    st.success("✅ 已成功上傳custom 組合")
                    st.dataframe(df)
        except Exception as e:
            st.error(f"❌ 上傳錯誤：{e}")

#匯入數據
weights = portfolio_configs[strategy]
tickers = list(weights.keys())

# 日期選擇(key=date2，和單一分析區隔)
START_DATE = st.date_input("開始日期(2016起):", value=pd.to_datetime("2020-01-01"), key="START_DATE2")
END_DATE = st.date_input("結束日期:", value=pd.to_datetime("2024-12-31"), key="END_DATE2")


# 指標顯示選項
show_ar = st.checkbox("顯示年化報酬率", value=True)
show_vol = st.checkbox("顯示年化波動度", value=True)
show_sharpe = st.checkbox("顯示 Sharpe Ratio", value=True)
show_mdd = st.checkbox("顯示最大回撤", value=True)

#各ETF占比圓餅圖
show_pie = st.checkbox("顯示各資產比重圓餅圖", value=False)

# main
if st.button("執行策略分析"):
    data = yf.download(tickers, start=START_DATE, end=END_DATE, auto_adjust=False)["Adj Close"]
  
    # 資料檢查
    if data.empty or data.isnull().values.any():
        st.error("❌ 某些資產資料下載失敗或缺漏，請檢查 Ticker 是否正確。")
        st.stop()
        
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
    
    # 勾選是否顯示特定績效指標
    if show_pie:
        st.subheader("各資產比重圓餅圖")
        pie_fig = pd.Series(weights).plot.pie(autopct='%1.1f%%', figsize=(5,5)).get_figure()
        st.pyplot(pie_fig)
    st.subheader("綜合策略績效")
    if show_ar:
        st.write(f"年化報酬率：{ar:.2%}")
    if show_vol:
        st.write(f"年化波動度：{vol:.2%}")
    if show_sharpe:
        st.write(f"Sharpe Ratio：{sharpe:.2f}")
    if show_mdd:
        st.write(f"最大回撤：{mdd:.2%}")








