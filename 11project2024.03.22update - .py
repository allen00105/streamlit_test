
# python做財報分析
# 1.	引入必要的套件：
# •開始時，引入用於網頁爬蟲和數據分析的相關Python套件，例如使用網頁爬蟲和Pandas進行數據處理。
# 2.	)網頁爬蟲：
# •使用網頁爬蟲技術(若太難就使用固定導入資料)從在線來源提取財務數據。您可以定位提供財報的特定網站。
# 3.	數據清理和準備：
# •清理和預處理提取的數據。這可能包括處理缺失值，轉換數據類型，並將數據組織成適合進行分析的格式。
# •例如：使用Pandas函數清理和結構化數據。
# 4.	數據分析：
# •利用Python的數據分析庫執行財務分析。Pandas、NumPy可用於各種分析任務。
# •例如：計算財務比率、趨勢或其他相關指標。
# 5.	可視化：
# •創建可視化圖表以更好地理解財務數據。例如：繪製財務趨勢，創建餅圖顯示支出結構等。
# 6.	自動化（不確定）：+
# •考慮使用腳本筆記本自動化過程。這有助於更輕鬆地再現和擴展分析

# 1. 引入必要的套件
# 引入了 Selenium、Pandas 和 requests 庫
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import pandas as pd
import time
import matplotlib.pyplot as plt

def get_financial_data():
    # 2. 網頁爬蟲
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.implicitly_wait(10)
    driver.get("https://mopsc.twse.com.tw/server-java/t164sb01?step=1&CO_ID=4430&SYEAR=2023&SSEASON=3&REPORT_ID=C#BalanceSheet")

    # 定位報表連結
    a_tag_ids = ['/html/body/div[2]/div[2]/ul/li[1]/a', '/html/body/div[2]/div[2]/ul/li[2]/a',
                 '/html/body/div[2]/div[2]/ul/li[3]/a', '/html/body/div[2]/div[2]/ul/li[4]/a']

    # 遍歷報表連結,獲取表格數據
    all_dfs = []
    for a_tag_id in a_tag_ids:
        a_tag = driver.find_element(By.XPATH, a_tag_id)
        a_tag.click()
        time.sleep(5)

        # 獲取報表 HTML 內容
        div_element = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]')
        table_elements = div_element.find_elements(By.TAG_NAME, 'table')
        table_elements = table_elements[0:4]  # 只取前 4 個表格

        # 使用 pandas 讀取表格
        dfs = [pd.read_html(table.get_attribute('outerHTML'))[0] for table in table_elements]
        all_dfs.extend(dfs)

    # 關閉瀏覽器
    driver.quit()

    # 3. 數據清理和準備
    # 合併所有表格數據為一個 DataFrame
    combined_df = pd.concat(all_dfs, ignore_index=True)

    return combined_df

def main():
    st.title("財務報表分析")

    # 獲取財務數據
    combined_df = get_financial_data()

    # 4. 數據分析
    # 找到包含 '應收帳款淨額' 的那一列
    accounts_receivable_col = combined_df[combined_df['資產負債表'].str.contains('應收帳款淨額')]

    # 如果找到該列,則獲取對應的數值
    if not accounts_receivable_col.empty:
        accounts_receivable_values = accounts_receivable_col.iloc[:, -1].tolist()  # 獲取整列數值
        st.write(f"應收帳款淨額: {', '.join(map(str, accounts_receivable_values))}")

        # 5. 可視化
        st.subheader("應收帳款淨額趨勢")
        years = accounts_receivable_col.iloc[:, 0].tolist()  # 獲取年份列表
        fig, ax = plt.subplots()
        ax.plot(years, accounts_receivable_values)
        ax.set_xlabel('年份')
        ax.set_ylabel('應收帳款淨額')
        st.pyplot(fig)
    else:
        st.write("未找到應收帳款淨額的數據")

    st.subheader("財務數據")
    st.dataframe(combined_df)

if __name__ == "__main__":
    main()