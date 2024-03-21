import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 加載CSV文件
data = pd.read_csv('onlinefoods.csv')

# Streamlit應用
st.title('Online Food Dataset')

# 顯示數據
st.subheader('數據概覽')
st.write(data)

# 選擇可視化列
viz_column = st.selectbox('選擇要可視化的列', data.columns)

# 根據選擇的列繪制圖表
if viz_column in data.select_dtypes(include=['int64', 'float64']).columns:
    st.subheader(f'{viz_column}分布')
    fig, ax = plt.subplots()
    ax = sns.histplot(data=data, x=viz_column, bins=20)
    st.pyplot(fig)
elif viz_column in data.select_dtypes(include=['object']).columns:
    st.subheader(f'{viz_column}分類統計')
    st.bar_chart(data[viz_column].value_counts())