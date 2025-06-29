#!/usr/bin/env python
# coding: utf-8

# In[1]:


##project01

#5:Streamlit 投資組合儀表板原型開發

#Step 5.1: imstall
# !pip install streamlit yfinance plotly pandas
# ↑install後記得註解掉，app會報錯


# In[9]:


#Step 5.2: import
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

#Step 5.3: 建立 Streamlit 主程式 app.py

st.title("📈 ETF 策略分析平台")

ticker = st.text_input("輸入 ETF 代碼，例如 VTI", "")
if ticker:
    data = yf.download(ticker, period="1y", auto_adjust=False)
    if data.empty:
        st.error("下載資料失敗，請確認代碼是否正確")
    else:
        st.line_chart(data['Adj Close'])



# In[ ]:




